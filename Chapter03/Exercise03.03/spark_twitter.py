from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, from_unixtime, unix_timestamp, window
from pyspark.sql.types import StructType, StructField, StringType

# the schema to parse a tweet in JSON format; we only need two columns
schema = StructType([StructField('created_at', StringType(), True),
                     StructField('text', StringType(), True)])

# launch a Spark session
spark = SparkSession.builder.appName('Packt').getOrCreate()

# get the raw data from a local socket
lines = spark.readStream.format('socket').option('host', 'localhost').option('port', 1234).load()


lines2 = lines.select(from_json('value', schema).alias('tweet'))

lines3 = lines2.select(from_unixtime(unix_timestamp(col('tweet.created_at'),
                                                    'EEE MMM dd HH:mm:ss ZZZZ yyyy')).alias('timestamp'),
                       'tweet.text')

lines4 = lines3.selectExpr('timestamp', 'text')

# To display the tweets without windowing:
# query = lines5.writeStream.outputMode('append').format('console').start()

# create a sliding window of 1 minute with a slide of 10 seconds, with a 'slack time' of 2 seconds
windowed = lines4\
    .withWatermark('timestamp', '2 seconds')\
    .groupBy(window('timestamp', '1 minute', '10 seconds'))

# count the tweets per window
counts_per_window = windowed.count()

query = counts_per_window.writeStream.outputMode('complete').format('console').start()

query.awaitTermination()
