from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession

KAFKA_TOPIC = "spark_topic"
KAFKA_SERVER = "localhost:9092"

# Create Spark Session
spark = SparkSession.builder \
    .master("local[1]") \
    .appName("hksharma.com") \
    .getOrCreate()

# Define schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", StringType(), True)
])

# Read CSV as a stream
source_data = spark.readStream \
    .format("csv") \
    .schema(schema) \
    .option("header", "true") \
    .option("path", "../../../resources/csv/") \
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
    .option("checkpointLocation", "../../resource/checkpoint/csv") \
    .start()

# Wait for the streaming query to finish
kafka_stream.awaitTermination()