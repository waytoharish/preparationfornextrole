from pyspark.sql import SparkSession


spark = SparkSession.builder\
 .master("local")\
 .appName('word_count')\
 .getOrCreate()


from pyspark.sql.functions import explode,split,col

df=spark.read.text("./words.txt")
#Apply Split, Explode and groupBy to get count()
df_count=(
  df.withColumn('word', explode(split(col('value'), ' ')))
    .groupBy('word')
    .count()
    .sort('count', ascending=False)
)

#Display Output
df_count.show()