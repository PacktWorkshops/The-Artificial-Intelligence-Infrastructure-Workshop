from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, window, col, expr, when, from_json, lit
from pyspark.sql.types import StructType, StructField, TimestampType, StringType
import json

spark = SparkSession.builder.appName('Packt').getOrCreate()

lines = spark.readStream.format('socket').option('host', 'localhost').option('port', 5557).load()


schema = StructType([StructField("created_at", TimestampType(), True),
                    StructField("text", StringType(), True)])

lines2 = lines.select(from_json(lines.value, schema).alias('tweet'))

lines3 = lines2.selectExpr('tweet.created_at', 'tweet.text')

lines4 = lines3.withColumn("count", lit(1))

windowed = lines4.groupBy(window("created_at", "1 minute", "10 seconds"))

counts = windowed.count()

# words = lines.select(explode(split(lines.value, " ")).alias('word'))

# wordCounts = words.groupBy('word').count()

query = counts.writeStream.outputMode('complete').format('console').start()

query.awaitTermination()
