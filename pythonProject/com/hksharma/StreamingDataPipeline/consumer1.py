from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, when
from pyspark.sql.types import StructType, StringType, IntegerType

# Get AWS credentials from environment variables
access_key = ""
secret_access_key = ""

# Create SparkSession with correct package versions for Spark 3.5.4
spark = SparkSession.builder \
    .appName("KafkaConsumerToS3") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,"
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "org.apache.hadoop:hadoop-common:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.481") \
    .config("spark.scala.version", "2.12.18") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_access_key) \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.sql.streaming.checkpointLocation", "s3a://flinkhksharmapoc/checkpoint/") \
    .getOrCreate()

# Define schema for the streaming data
schema = StructType() \
    .add("userid", StringType()) \
    .add("user_location", StringType()) \
    .add("channelid", IntegerType()) \
    .add("genre", StringType()) \
    .add("lastactive", StringType()) \
    .add("title", StringType()) \
    .add("watchfrequency", IntegerType()) \
    .add("etags", StringType())

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "streamTopic") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse the JSON data
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Add impression column
netflix_df = parsed_df.withColumn('impression',
                                  when(parsed_df['watchfrequency'] < 3, "neutral")
                                  .when(((parsed_df['watchfrequency'] >= 3) &
                                         (parsed_df['watchfrequency'] <= 10)), "like")
                                  .otherwise("favorite")
                                  )

# Drop the etags column
netflix_transformed_df = netflix_df.drop('etags')

# Write to S3
output_path = "s3a://flinkhksharmapoc/streamData/"

try:
    query = netflix_transformed_df.writeStream \
        .format("parquet") \
        .outputMode("append") \
        .option("path", output_path) \
        .start()

    query.awaitTermination()

except Exception as e:
    print(f"Error occurred: {str(e)}")
    spark.stop()
