import os
from pyspark.conf import SparkConf
from pyspark.sql.functions import (col, from_json, to_timestamp)
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, StructField, TimestampType, IntegerType

CATALOG = "glue_catalog"
ICEBERG_S3_PATH = "data-lake-apache-iceberg"
DATABASE = "iceberg"
TABLE_NAME = "tempsensors"
PRIMARY_KEY = "client_id"
DYNAMODB_LOCK_TABLE = "iceberg - lock"
KAFKA_TOPIC_NAME = "KafkaGlueIcebergTopic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
STARTING_OFFSETS_OF_KAFKA_TOPIC = "latest"
AWS_REGION = "ap-south-1"
WINDOW_SIZE = "100 seconds"
TEMP_DIR = "s3a://flinkhksharmapoc/data-lake-apache-iceberg/temporary/"
JOB_NAME = "load_streaming_data_glue_job"

ACCESS_KEY = ""
SECRET_ACCESS_KEY = ""

packages = [
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.3",
    "org.apache.iceberg:iceberg-aws-bundle:1.4.3",
    "org.apache.spark:spark-avro_2.12:3.5.0",
    "com.amazonaws:aws-java-sdk-bundle:1.12.262",
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4",
    "org.apache.kafka:kafka-clients:3.5.0",
    "org.apache.commons:commons-pool2:2.12.0",
    "org.apache.hadoop:hadoop-aws:3.3.4",
    "org.apache.hadoop:hadoop-common:3.3.4"

]


# def setSparkIcebergConf() -> SparkConf:
#     conf_list = [
#         (f"spark.sql.catalog.{CATALOG}", "org.apache.iceberg.spark.SparkCatalog"),
#         (f"spark.sql.catalog.{CATALOG}.warehouse", ICEBERG_S3_PATH),
#         (f"spark.sql.catalog.{CATALOG}.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog"),
#         (f"spark.sql.catalog.{CATALOG}.io-impl", "org.apache.iceberg.aws.s3.S3FileIO"),
#         (f"spark.sql.catalog.{CATALOG}.lock-impl", "org.apache.iceberg.aws.glue.DynamoLockManager"),
#         (f"spark.sql.catalog.{CATALOG}.lock.table", DYNAMODB_LOCK_TABLE),
#         ("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"),
#         ("spark.sql.iceberg.handle-timestamp-without-timezone", "true")
#     ]
#     spark_conf = SparkConf().setAll(conf_list)
#     return spark_conf
#
#
# conf = setSparkIcebergConf()


# # Create the SparkSession
# spark = SparkSession.builder \
#     .appName("Iceburg Basics") \
#     .master("local[*]") \
#     .config("spark.jars.packages", ",".join(packages)) \
#     .config(conf=conf) \
#     .getOrCreate()




#
# # Set the Spark + Glue context
# conf = setSparkIcebergConf()
# sc = SparkContext(conf=conf).getOrCreate
#
# #glueContext = GlueContext(sc)
# spark = sc.spark_session
# #job = Job(glueContext)
# #job.init(args['JOB_NAME'], args)

spark = SparkSession.builder \
    .config("spark.sql.defaultCatalog", "glue_catalog") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.glue_catalog.warehouse", "s3a://flinkhksharmapoc/iceburg-warehouse") \
    .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.secret.key", SECRET_ACCESS_KEY) \
    .config("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
    .config("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .config("spark.sql.source.partitionOverviewMode", "dynamic") \
    .config("hive.metastore.client.factory.class",
            "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory") \
    .enableHiveSupport() \
    .getOrCreate()

# options_read = {
#     "kafka.bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
#     "subscribe": KAFKA_TOPIC_NAME,
#     "startingOffsets": STARTING_OFFSETS_OF_KAFKA_TOPIC
# }

options_read = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'testGrouID',
    'subscribe': KAFKA_TOPIC_NAME,
    'auto.offset.reset': STARTING_OFFSETS_OF_KAFKA_TOPIC
}

schema = StructType([
    StructField("client_id", StringType(), False),
    StructField("timestamp", TimestampType(), True),
    StructField("humidity", IntegerType(), False),
    StructField("temperature", IntegerType(), False),
    StructField("pressure", IntegerType(), False),
    StructField("pitch", StringType(), False),
    StructField("roll", StringType(), False),
    StructField("yaw", StringType(), False),
    StructField("count", IntegerType(), False),
])

spark.sql("""
CREATE TABLE IF NOT EXISTS glue_catalog.iceberg.tempsensors (
   client_id string,
   timestamp timestamp,
   humidity int,
   temperature int,
   pressure int,
   pitch string,
   roll string,
   yaw string,
   count bigint)
USING iceberg
PARTITIONED BY (days(timestamp))
LOCATION 's3a://flinkhksharmapoc/tempsensors'
TBLPROPERTIES (
  'write.format.default' = 'parquet',
  'write.target-file-size-bytes' = '536870912',
  'format-version' = '2'
)
""")

# Verify the table structure
spark.sql("DESCRIBE TABLE glue_catalog.iceberg.tempsensors").show(truncate=False)

streaming_data = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC_NAME) \
    .load()


stream_data_df = streaming_data \
    .select(from_json(col("value").cast("string"), schema).alias("source_table")) \
    .select("source_table.*") \
    .withColumn('timestamp', to_timestamp(col('timestamp'), 'yyyy-MM-dd HH:mm:ss'))

table_id = f"{CATALOG}.{DATABASE}.{TABLE_NAME}"
checkpointPath = os.path.join(TEMP_DIR, JOB_NAME, "checkpoint/")

# Writing against partitioned table
query = stream_data_df.writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .trigger(processingTime=WINDOW_SIZE) \
    .option("path", table_id) \
    .option("fanout-enabled", "true") \
    .option("checkpointLocation", checkpointPath) \
    .toTable(table_id)

query.awaitTermination()
