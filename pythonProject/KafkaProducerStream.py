import time
import random
from faker import Faker
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import json
from pyspark.sql.functions import col, to_json, struct




fake = Faker()
# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'spark_topic'
}

schema = StructType() \
    .add("userid", StringType()) \
    .add("user_location", StringType()) \
    .add("channelid", IntegerType()) \
    .add("genre", StringType()) \
    .add("lastactive", StringType()) \
    .add("title", StringType()) \
    .add("watchfrequency", IntegerType()) \
    .add("etags", StringType())


# Kafka producer function
def produce():
    # producer = Producer(conf)
    KAFKA_TOPIC = "spark_topic"
    KAFKA_SERVER = "localhost:9092"

    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("hksharma.com") \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.4')\
        .getOrCreate()

    while True:  # Run indefinitely until manually stopped
        # Produce some dummy data to Kafka topic
        netflix_data = {
            'userid': fake.uuid4(),
            'user_location': random.choice(['Nepal', 'USA', 'India', 'China', 'Belgium', 'Canada', 'Switzerland']),
            'channelid': fake.random_int(min=1, max=50),
            'genre': random.choice(['thriller', 'comedy', 'romcom', 'fiction']),
            'lastactive': fake.date_time_between(start_date='-10m', end_date='now').isoformat(),
            'title': fake.name(),
            'watchfrequency': fake.random_int(min=1, max=10),
            'etags': fake.uuid4()
        }
        data = [netflix_data]
        data_df = spark.createDataFrame(data, schema=schema)
        kafka_df = data_df.select(
            col("userid").cast("string").alias("key"),
            to_json(struct("*")).alias("value")
        )

        kafka_df.show()

        kafka_df.selectExpr("CAST(value AS STRING)") \
            .write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_SERVER) \
            .option("topic", KAFKA_TOPIC) \
            .save()
    # schema1 = StructType([
    #     StructField("id", IntegerType(), False),
    #     StructField("message", StringType(), True)
    # ])
    # data = [(4, "message1"),
    #         (5, "message2"),
    #         (6, "message3")]

    #data_df = spark.createDataFrame(data, schema=schema1)

    # Convert to Kafka format

        #chatgpt_df = spark.createDataFrame(netflix_data)
        # chatgpt_df.selectExpr("CAST(value AS STRING)")\
        # .write.format("kafka")\
        # .options("kafka.bootstrap.servers", "localhost:9092")\
        # .option("topic",

    # producer.produce('streamTopic', value=json.dumps(netflix_data))


       # print(netflix_data)
        #time.sleep(1)
        #producer.flush()


# Call the producer function
produce()
