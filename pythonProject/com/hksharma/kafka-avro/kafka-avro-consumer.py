import os

from pyspark.sql import SparkSession
import json

from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col


def get_resource_path(filename):
    """Get the absolute path of a resource file"""
    BASE_DIR = "/Users/hkshar/PycharmProjects/pythonProject"
    SCHEMA_PATH = os.path.join(BASE_DIR, "resources", filename)
    # Add error handling
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
    # Rest of your code...
    return os.path.abspath(SCHEMA_PATH)


packages = [
    "org.apache.spark:spark-avro_2.12:3.5.0",
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4",
]

# Create Spark Session
spark = SparkSession.builder \
    .master("local") \
    .appName("SparkByExample.com") \
    .config("spark.jars.packages", ",".join(packages)) \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

schema_path = get_resource_path("person.avsc")

if not os.path.exists(schema_path):
    raise FileNotFoundError(f"Schema file not found at {schema_path}")

    # Read the schema
with open(schema_path, "r") as schema_file:
    json_format_schema = schema_file.read()

# Create streaming DataFrame from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "avro_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Print Kafka schema
df.printSchema()

# Convert Avro data to DataFrame
person_df = df.select(from_avro(col("value"), json_format_schema).alias("person")) \
    .select("person.*")

# Print schema of the transformed DataFrame
person_df.printSchema()

# Write streaming data to console
query = person_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# Wait for the streaming to finish
query.awaitTermination()
