from pyspark.sql import SparkSession



spark = (SparkSession.builder.appName("KafkaStream")
         .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.4')
         .getOrCreate())



df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "spark_topic") \
    .option("startingOffsets", "latest")  \
    .load()



# Process the DataFrame as needed

df.printSchema()

df.writeStream \
.format("console") \
.outputMode("append") \
.start() \
.awaitTermination()