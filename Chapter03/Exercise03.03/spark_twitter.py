from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, lit, from_unixtime, unix_timestamp
from pyspark.sql.types import StructType, StructField, StringType

spark = SparkSession.builder.appName('Packt').getOrCreate()

lines = spark.readStream.format('socket').option('host', 'localhost').option('port', 5557).load()


schema = StructType([StructField('created_at', StringType(), True),
                    StructField('text', StringType(), True)])

lines2 = lines.select(from_json('value', schema).alias('tweet'))

lines3 = lines2.select('tweet.created_at', 'tweet.text',
                       from_unixtime(unix_timestamp(col('tweet.created_at'),
                                                    'EEE MMM dd HH:mm:ss ZZZZ yyyy')).alias('timestamp'))

lines4 = lines3.selectExpr('created_at', 'timestamp', 'text')

lines5 = lines4.withColumn('count', lit(1))

query = lines5.writeStream.outputMode('append').format('console').start()

#windowed = lines4.groupBy(window('created_at', '1 minute', '10 seconds'))

#counts = windowed.count()

#query = counts.writeStream.outputMode('complete').format('console').start()

query.awaitTermination()
