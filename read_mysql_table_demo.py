from pyspark.sql import SparkSession

if __name__ == "__main__":
    print("Mysql Demo: Application Started.")

    '''spark = SparkSession \
        .builder \
        .appName("Read mysql table demo") \
        .config("spark.jars",
                "file:///home/datamaking/softwares/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46.jar") \
        .config("spark.executor.extraClassPath",
                "file:///home/datamaking/softwares/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46.jar") \
        .config("spark.executor.extraLibrary",
                "file:///home/datamaking/softwares/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46.jar") \
        .config("spark.driver.extraClassPath",
                "file:///home/datamaking/softwares/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46.jar") \
        .enableHiveSupport() \
        .getOrCreate() '''

    spark = SparkSession \
        .builder \
        .appName("Read mysql table demo") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    mysql_db_driver_class = "com.mysql.jdbc.Driver"
    table_name = "users"
    hostname = "localhost"
    port_no = str(3306)
    user_name = "root"
    password = "datamaking"
    database_name = "test_db"

    mysql_select_query = None
    mysql_select_query = "(select * from " + table_name + ") as users"
    print("Printing mysql_select_query:")
    print(mysql_select_query)

    mysql_jdbc_url = "jdbc:mysql://" + hostname + ":" + port_no + "/" + database_name
    print("Printing JDBC URL: " + mysql_jdbc_url)

    trans_detail_tbl_data_df = spark.read.format("jdbc") \
        .option("url",mysql_jdbc_url) \
        .option("driver",mysql_db_driver_class) \
        .option("dbtable",mysql_select_query) \
        .option("user",user_name) \
        .option("password",password) \
        .load()

    trans_detail_tbl_data_df.show(10, 0)
    print("Mysql Demo: Application Completed.")



