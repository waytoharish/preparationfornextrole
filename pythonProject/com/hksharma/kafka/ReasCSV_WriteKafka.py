from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession
import os
import shutil

KAFKA_TOPIC = "spark_topic"
KAFKA_SERVER = "localhost:9092"

BASE_DIR = "/Users/hkshar/PycharmProjects/pythonProject/resources"
ORIGINAL_CSV = os.path.join(BASE_DIR, "peoples.csv")
INPUT_DIR = os.path.join(BASE_DIR, "streaming_input")
CHECKPOINT_DIR = os.path.join(BASE_DIR, "checkpoint")

def setup_environment():
    """Setup the directory structure correctly"""
    for directory in [INPUT_DIR, CHECKPOINT_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    if os.path.exists(ORIGINAL_CSV):
        shutil.copy2(ORIGINAL_CSV, os.path.join(INPUT_DIR, "peoples.csv"))
        print(f"Copied CSV file to streaming directory")
    else:
        raise FileNotFoundError(f"Original CSV not found at {ORIGINAL_CSV}")

# Setup the environment
setup_environment()

# Define all required packages
packages = [
    "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0",
    "org.apache.kafka:kafka-clients:3.5.0",
    "org.apache.commons:commons-pool2:2.12.0"
]

# Create Spark Session with stable version dependencies
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("KafkaStreamingApp") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

# Define schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", StringType(), True)
])

try:
    # Read streaming data
    source_data = spark.readStream \
        .format("csv") \
        .schema(schema) \
        .option("header", "true") \
        .option("maxFilesPerTrigger", 1) \
        .option("path", INPUT_DIR) \
        .load()

    # Add timestamp column
    transformed_data = source_data.withColumn("timestamp", current_timestamp())

    # Write to Kafka
    kafka_stream = transformed_data \
        .selectExpr("to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_SERVER) \
        .option("topic", KAFKA_TOPIC) \
        .option("checkpointLocation", CHECKPOINT_DIR) \
        .start()

    print("Streaming started successfully")
    kafka_stream.awaitTermination()

except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    print(f"Full stacktrace: {traceback.format_exc()}")
    if 'kafka_stream' in locals():
        kafka_stream.stop()
    spark.stop()
