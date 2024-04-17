from pyspark.sql import SparkSession
import boto3

def create_athena_table(df, partition_column, s3_path, database_name, table_name):
    # Ensure the DataFrame column names are compatible with Athena (lowercase and without spaces)
    for col in df.columns:
        new_col_name = col.lower().replace(' ', '_')
        df = df.withColumnRenamed(col, new_col_name)
    
    # Save the DataFrame to S3 as Parquet files, partitioned by the specified column
    df.write.mode('overwrite').partitionBy(partition_column).parquet(s3_path)
    
    # Athena compatible schema creation from DataFrame schema
    schema_statement = ', '.join([f"{col.name} {spark_to_athena_type(col.dataType)}" for col in df.schema])
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

def spark_to_athena_type(spark_type):
    # Convert PySpark types to Athena types
    mapping = {
        'IntegerType': 'int',
        'LongType': 'bigint',
        'DoubleType': 'double',
        'DecimalType': 'decimal',
        'StringType': 'string',
        'DateType': 'date',
        'TimestampType': 'timestamp',
        'BooleanType': 'boolean'
    }
    return mapping.get(spark_type.simpleString(), 'string')  # Default to string if no exact match found

# Example usage:
# Initialize your Spark session, e.g.:
# spark = SparkSession.builder.appName("Athena Table Creation").getOrCreate()

# Assume df is your DataFrame loaded/defined previously
# create_athena_table(df, 'partition_col', 's3://your-bucket/your-path/', 'your_database', 'your_table')
