from pyspark.sql import SparkSession
from pyspark.sql.types import *
import boto3

def spark_to_athena_type(spark_type):
    # Base mapping for simple data types
    mapping = {
        'integer': 'int',
        'long': 'bigint',
        'double': 'double',
        'decimal': 'decimal',
        'string': 'string',
        'date': 'date',
        'timestamp': 'timestamp',
        'boolean': 'boolean',
        'binary': 'binary',
        'float': 'float'
    }
    
    # Handling complex data types recursively
    if isinstance(spark_type, StructType):
        return 'struct<' + ', '.join([f"{field.name}:{spark_to_athena_type(field.dataType)}" for field in spark_type.fields]) + '>'
    elif isinstance(spark_type, ArrayType):
        return 'array<' + spark_to_athena_type(spark_type.elementType) + '>'
    elif isinstance(spark_type, MapType):
        return f"map<{spark_to_athena_type(spark_type.keyType)}, {spark_to_athena_type(spark_type.valueType)}>"
    
    return mapping.get(spark_type.typeName(), 'string')  # Default to string if no exact match found

def create_athena_table(df, partition_column, s3_path, database_name, table_name):
    # Normalize column names for Athena compatibility
    df = df.select([col(c).alias(c.lower().replace(' ', '_').replace('.', '_')) for c in df.columns])

    # Save the DataFrame to S3 as Parquet files, partitioned by the specified column
    df.write.mode('overwrite').partitionBy(partition_column).parquet(s3_path)
    
    # Athena compatible schema creation from DataFrame schema
    schema_statement = ', '.join([f"{field.name} {spark_to_athena_type(field.dataType)}" for field in df.schema.fields if field.name != partition_column])
    partition_statement = f"PARTITIONED BY ({partition_column} {spark_to_athena_type(df.schema[partition_column].dataType)})"

    # SQL statement to create the Athena table
    create_table_statement = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (
        {schema_statement}
    )
    {partition_statement}
    STORED AS PARQUET
    LOCATION '{s3_path}'
    """

    # Execute the create table statement in Athena using boto3
    client = boto3.client('athena', region_name='your-region')
    response = client.start_query_execution(
        QueryString=create_table_statement,
        QueryExecutionContext={
            'Database': database_name
        },
        ResultConfiguration={
            'OutputLocation': 's3://your-output-bucket/path-to-query-results/'
        }
    )
    print("Athena query started, execution ID:", response['QueryExecutionId'])

# Example usage:
# spark = SparkSession.builder.appName("Athena Table Creation").getOrCreate()
# Assume df is your DataFrame loaded/defined previously
# create_athena_table(df, 'partition_column_name', 's3://your-bucket/your-path/', 'your_database', 'your_table')
