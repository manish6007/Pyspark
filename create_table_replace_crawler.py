import boto3

def check_if_table_exists(database_name, table_name):
    """
    Check if a table exists in the AWS Glue Data Catalog.

    :param database_name: The name of the Glue database.
    :param table_name: The name of the table to check.
    :return: True if the table exists, False otherwise.
    """
    client = boto3.client('glue')

    try:
        response = client.get_table(DatabaseName=database_name, Name=table_name)
        return True  # If the call succeeds, the table exists
    except client.exceptions.EntityNotFoundException:
        return False  # If EntityNotFoundException is raised, the table does not exist
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False  # In case of other exceptions, return False

def delete_glue_table(database_name, table_name):
    """
    Delete a table from the AWS Glue Data Catalog.

    :param database_name: The name of the Glue database.
    :param table_name: The name of the table to be deleted.
    """
    client = boto3.client('glue')
    
    try:
        response = client.delete_table(DatabaseName=database_name, Name=table_name)
        print(f"Table {table_name} successfully deleted from database {database_name}.")
    except client.exceptions.EntityNotFoundException:
        print(f"Table {table_name} not found in database {database_name}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_partitioned_glue_table(database_name, table_name, s3_location, columns, partition_keys):
    """
    Create a partitioned table in the AWS Glue Data Catalog.

    :param database_name: The name of the Glue database.
    :param table_name: The name of the new table.
    :param s3_location: The S3 location of the data (e.g., 's3://your-bucket/path/to/data/').
    :param columns: A list of column definitions as expected by Glue.
    :param partition_keys: A list of partition key definitions.
    """
    client = boto3.client('glue')

    # Separate the partition keys from the regular columns
    # Check if the table exists and delete it if it does
    if check_if_table_exists(database_name, table_name):
        delete_glue_table(database_name, table_name)
    data_columns = [col for col in columns if col['Name'] not in partition_keys]
    partition_columns = [{'Name': key, 'Type': 'string'} for key in partition_keys]

    try:
        response = client.create_table(
            DatabaseName=database_name,
            TableInput={
                'Name': table_name,
                'StorageDescriptor': {
                    'Columns': data_columns,
                    'Location': s3_location,
                    'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
                        'Parameters': {
                            'serialization.format': '1'
                        }
                    },
                },
                'PartitionKeys': partition_columns,
                'TableType': 'EXTERNAL_TABLE',
                'Parameters': {
                    'classification': 'parquet',
                    'compressionType': 'none'
                }
            }
        )
        print(f"Partitioned table {table_name} created successfully in database {database_name}.")
    except Exception as e:
        print(f"An error occurred while creating the partitioned table: {str(e)}")

# Example usage
database_name = 'test_data'
table_name = 'test'
s3_location = 's3://cf-templates-rvk6ey9p6t0j-us-east-1/test/'

# Define the list of partition key names
partition_keys = ['year', 'month', 'day']

# Define your columns including partition columns
columns = [
    {'Name': 'Invoice_ID', 'Type': 'string'},
    {'Name': 'Branch', 'Type': 'string'},
    {'Name': 'City', 'Type': 'string'},
    {'Name': 'Customer_type', 'Type': 'string'},
    {'Name': 'Gender', 'Type': 'string'},
    {'Name': 'Product_line', 'Type': 'string'},
    {'Name': 'Unit_price', 'Type': 'decimal(10,2)'},
    {'Name': 'Quantity', 'Type': 'int'},
    {'Name': 'Tax_5percent', 'Type': 'decimal(10,2)'},
    {'Name': 'Total', 'Type': 'decimal(10,2)'},
    {'Name': 'Time', 'Type': 'string'},  # Glue does not support time data type, hence representing as string
    {'Name': 'Payment', 'Type': 'string'},
    {'Name': 'cogs', 'Type': 'decimal(10,2)'},
    {'Name': 'gross_margin_percentage', 'Type': 'decimal(10,2)'},
    {'Name': 'gross_income', 'Type': 'decimal(10,2)'},
    {'Name': 'Rating', 'Type': 'decimal(10,2)'},
    {'Name': 'year', 'Type': 'string'},
    {'Name': 'month', 'Type': 'string'},
    {'Name': 'day', 'Type': 'string'}
]

create_partitioned_glue_table(database_name, table_name, s3_location, columns, partition_keys)

#Afer adding partition run below command on Athena
#MSCK REPAIR TABLE test;
