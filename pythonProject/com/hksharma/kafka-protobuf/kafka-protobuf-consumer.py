import os

from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col
from pyspark.sql.protobuf.functions import from_protobuf


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

# Create Spark Session
spark = SparkSession.builder \
    .master("local") \
    .appName("SparkByExample.com") \
    .config("spark.jars.packages", ",".join(packages)) \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

schema_path = get_resource_path("person.pb")

if not os.path.exists(schema_path):
    raise FileNotFoundError(f"Schema file not found at {schema_path}")

# Create streaming DataFrame from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "protobuf_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Print Kafka schema
df.printSchema()

# Convert Avro data to DataFrame
person_df = (df.select(from_protobuf(col("value"), "Person", schema_path).alias("person"))
             .select("person.*"))

# Print schema of the transformed DataFrame
person_df.printSchema()

# Write streaming data to console
query = person_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# Wait for the streaming to finish
query.awaitTermination()
