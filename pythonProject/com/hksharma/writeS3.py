from typing import *
from pyspark import Row
from pyspark.sql import SparkSession

access_key = ""
secret_access_key = ""


# Get credentials from environment variables


packages = [
    "org.apache.spark:spark-avro_2.12:3.5.0",
    "org.apache.hudi:hudi-spark3.5-bundle_2.12:1.0.0",
    "org.apache.hadoop:hadoop-aws:3.3.4",
    "org.apache.hadoop:hadoop-common:3.3.4",
    "com.amazonaws:aws-java-sdk-bundle:1.12.262"
]

# Create the SparkSession
spark = SparkSession.builder \
    .appName("Hudi Basics") \
    .master("local[*]") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.jars.repositories", "https://repo.maven.apache.org/maven2") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_access_key) \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.hadoop.fs.s3a.path.style.access", "True") \
    .config("spark.sql.legacy.createHiveTableByDefault", "false") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

# Create a DataFrame
inputDF = spark.createDataFrame(
    [
        ("100", "2015-01-01", "2015-01-01T13:51:39.340396Z"),
        ("101", "2015-01-01", "2015-01-01T12:14:58.597216Z"),
        ("102", "2015-01-01", "2015-01-01T13:51:40.417052Z"),
        ("103", "2015-01-01", "2015-01-01T13:51:40.519832Z"),
        ("104", "2015-01-02", "2015-01-01T12:15:00.512679Z"),
        ("105", "2015-01-02", "2015-01-01T13:51:42.248818Z"),
    ],
    ["id", "creation_date", "last_update_time"]
)

# Hudi options without Hive sync
hudiOptions = {
    'hoodie.table.name': 'pyspark_hudi_table',
    'hoodie.datasource.write.recordkey.field': 'id',
    'hoodie.datasource.write.partitionpath.field': 'creation_date',
    'hoodie.datasource.write.precombine.field': 'last_update_time',
    'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
    'hoodie.datasource.write.operation': 'upsert',
    'hoodie.cleaner.policy': 'KEEP_LATEST_COMMITS',
    'hoodie.cleaner.commits.retained': 3
}

# Write the DataFrame to Hudi
inputDF.write \
    .format('hudi') \
    .options(**hudiOptions) \
    .mode('overwrite') \
    .save('s3a://flinkhksharmapoc/myhudidataset/')

# To read the data back
readDF = spark.read \
    .format('hudi') \
    .load('s3a://flinkhksharmapoc/myhudidataset/')

readDF.show()

# Clean up
spark.stop()
