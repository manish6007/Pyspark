import sys
import boto3
import psycopg2
from awsglue.utils import getResolvedOptions

# Get arguments
args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 'source_database', 'source_schema', 'target_schema', 'secret_name', 'btb_grp'
])

source_database = args['source_database']
source_schema = args['source_schema']
target_schema = args['target_schema']
secret_name = args['secret_name']
btb_grp = args['btb_grp']

# Initialize a session using Amazon Secrets Manager
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager'
)

# Retrieve secret value
secret = client.get_secret_value(SecretId=secret_name)
secret_dict = json.loads(secret['SecretString'])

# Extract Redshift details from the secret
redshift_user = secret_dict['username']
redshift_password = secret_dict['password']
redshift_host = secret_dict['host']
redshift_port = secret_dict['port']

# Connect to Redshift
conn = psycopg2.connect(
    dbname=source_database,
    user=redshift_user,
    password=redshift_password,
    host=redshift_host,
    port=redshift_port
)
conn.autocommit = True
cursor = conn.cursor()

# Fetch all tables in the source schema
cursor.execute(f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = '{source_schema}'
    AND table_type = 'BASE TABLE'
""")
tables = cursor.fetchall()

# Loop through each table to create views and grant permissions
for table in tables:
    table_name = table[0]
    view_name = table_name

    # Create view in the target schema
    create_view_sql = f"""
    CREATE OR REPLACE VIEW {target_schema}.{view_name} AS
    SELECT * FROM {source_database}.{source_schema}.{table_name}
    """
    cursor.execute(create_view_sql)

    # Grant SELECT permission on the view to the group
    grant_select_sql = f"""
    GRANT SELECT ON {target_schema}.{view_name} TO GROUP {btb_grp}
    """
    cursor.execute(grant_select_sql)

# Close cursor and connection
cursor.close()
conn.close()
