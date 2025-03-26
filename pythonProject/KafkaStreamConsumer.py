from pyspark.sql import SparkSession


KAFKA_TOPIC = "spark_topic"
KAFKA_SERVER = "localhost:9092"

# creating an instance of SparkSession
spark_session = SparkSession \
    .builder \
    .appName("Python Spark create RDD") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.4') \
    .getOrCreate()

# Subscribe to 1 topic
df = spark_session \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")\
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("topic", "spark_stream_topic") \
    .option("checkpointLocation", "resource") \
    .start()

spark_session.streams.awaitAnyTermination()

