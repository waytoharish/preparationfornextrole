import os

from pyspark.sql import SparkSession
from pyspark.sql.protobuf.functions import to_protobuf
from pyspark.sql.types import IntegerType, StringType, StructType, DoubleType
from pyspark.sql.functions import struct, col, from_json


def get_resource_path(filename):
    """Get the absolute path of a resource file"""
    BASE_DIR = "/Users/hkshar/PycharmProjects/pythonProject"
    SCHEMA_PATH = os.path.join(BASE_DIR, "resources/proto", filename)
    # Add error handling
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
    # Rest of your code...
    return os.path.abspath(SCHEMA_PATH)


packages = [
    "org.apache.spark:spark-protobuf_2.12:3.5.4",
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4",
]

# Create Spark Session with stable version dependencies
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("KafkaStreamingApp") \
    .config("spark.jars.packages", ",".join(packages)) \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "json_topic") \
    .option("startingOffsets", "latest") \
    .load()

df.printSchema()

schema = StructType() \
    .add("id", IntegerType()) \
    .add("firstname", StringType()) \
    .add("middlename", StringType()) \
    .add("lastname", StringType()) \
    .add("dob_year", IntegerType()) \
    .add("dob_month", IntegerType()) \
    .add("gender", StringType()) \
    .add("salary", DoubleType())

parsed_df = (df.selectExpr("CAST(value AS STRING)")
             .select(from_json(col("value"), schema).alias("data")))

schema_path = get_resource_path("person.pb")

if not os.path.exists(schema_path):
    raise FileNotFoundError(f"Schema file not found at {schema_path}")


parsed_df.select(to_protobuf(struct("data.*"), "Person", schema_path).alias("value")) \
    .writeStream \
    .format("kafka") \
    .outputMode("append") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "protobuf_topic") \
    .option("checkpointLocation", "/Users/hkshar/PycharmProjects/pythonProject/tmp") \
    .start().awaitTermination()
