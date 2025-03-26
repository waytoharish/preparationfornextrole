from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import to_avro
from pyspark.sql.types import IntegerType, StringType, StructType
from pyspark.sql.functions import struct, col, from_json

packages = [
    "org.apache.spark:spark-avro_2.12:3.5.0",
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
    .option("startingOffsets", "earliest") \
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
    .add("salary", IntegerType())

personDF = (df.selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), schema).alias("data")))

personDF.select(to_avro(struct("data.*")).alias("value")) \
    .writeStream \
    .format("kafka")  \
    .outputMode("append") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "avro_topic") \
    .option("checkpointLocation", "/Users/hkshar/PycharmProjects/pythonProject/tmp") \
    .start() \
    .awaitTermination()
