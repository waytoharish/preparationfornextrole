from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType, BooleanType, DecimalType
from pyspark.sql.functions import to_json, struct, col
import os
import shutil

BASE_DIR = "/Users/hkshar/PycharmProjects/pythonProject/resources/json"
ORIGINAL_JSON = os.path.join(BASE_DIR, "zipcodes.json")
INPUT_DIR = os.path.join(BASE_DIR, "streaming_json")
CHECKPOINT_DIR = os.path.join(BASE_DIR, "checkpoint")

KAFKA_TOPIC = "spark_topic"
KAFKA_SERVER = "localhost:9092"


def setup_environment():
    """Setup the directory structure correctly"""
    for directory in [INPUT_DIR, CHECKPOINT_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    if os.path.exists(ORIGINAL_JSON):
        shutil.copy2(ORIGINAL_JSON, os.path.join(INPUT_DIR, "zipcodes.json"))
        print(f"Copied JSON file to streaming directory")
    else:
        raise FileNotFoundError(f"Original JSON not found at {ORIGINAL_JSON}")


# Setup the environment
setup_environment()

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

jsonSchema = StructType([
    StructField("RecordNumber", IntegerType(), True),
    StructField("Zipcode", IntegerType(), True),
    StructField("ZipCodeType", StringType(), True),
    StructField("City", StringType(), True),
    StructField("State", StringType(), True),
    StructField("LocationType", StringType(), True),
    StructField("Lat", DecimalType(), True),
    StructField("Long", DecimalType(), True),
    StructField("Xaxis", DecimalType(), True),
    StructField("Yaxis", DecimalType(), True),
    StructField("Zaxis", DecimalType(), True),
    StructField("WorldRegion", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("LocationText", StringType(), True),
    StructField("Location", StringType(), True),
    StructField("Decommisioned", BooleanType(), True),
])

try:
    # Read streaming data
    streamingInputDF = (
        spark
        .readStream
        .schema(jsonSchema)  # Set the schema of the JSON data
        .option("maxFilesPerTrigger", 1)  # Treat a sequence of files as a stream by picking one file at a time
        .json(INPUT_DIR)
    )

    # Convert all columns to JSON string
    kafka_df = streamingInputDF.select(
        to_json(struct([streamingInputDF[x] for x in streamingInputDF.columns])).alias("value")
    )

    # Write to Kafka
    kafka_stream = kafka_df \
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
        streamingInputDF.stop()
    spark.stop()


