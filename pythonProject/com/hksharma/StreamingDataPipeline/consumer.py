from confluent_kafka import Consumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, when
from pyspark.sql.types import StructType, StringType, IntegerType

# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic = 'streamTopic'
group_id = 'group_id'

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

# Create Kafka consumer
consumer = Consumer(conf)
consumer.subscribe([topic])

access_key = ""
secret_access_key = ""


# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaConsumerToS3") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,"
                                   "org.apache.hadoop:hadoop-aws:3.4.1,"
                                   "com.amazonaws:aws-java-sdk-bundle:1.12.780") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_access_key) \
    .config("spark.hadoop.fs.s3a.path.style.access", "True") \
    .getOrCreate()

schema = StructType() \
    .add("userid", StringType()) \
    .add("user_location", StringType()) \
    .add("channelid", IntegerType()) \
    .add("genre", StringType()) \
    .add("lastactive", StringType()) \
    .add("title", StringType()) \
    .add("watchfrequency", IntegerType()) \
    .add("etags", StringType())

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", bootstrap_servers) \
    .option("subscribe", topic) \
    .load()


parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Perform necessary transformations on the parsed data
netflix_df = parsed_df.withColumn('impression',
    when(parsed_df['watchfrequency'] < 3, "neutral")
    .when(((parsed_df['watchfrequency'] >= 3) & (parsed_df['watchfrequency'] <= 10)), "like")
    .otherwise("favorite")
)

# Drop the etags values
netflix_transformed_df = netflix_df.drop('etags')

output_path = "s3a://flinkhksharmapoc/streamData/"
query = netflix_transformed_df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("checkpointLocation", "s3a://flinkhksharmapoc/checkpoint/") \
    .start(output_path)

# Await termination
query.awaitTermination()




