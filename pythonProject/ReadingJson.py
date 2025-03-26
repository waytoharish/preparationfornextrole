from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .master("local[1]") \
    .appName("hksharma.com") \
    .getOrCreate()

df = spark.read.json("resources/zipcodes.json")
df.printSchema()
df.show()