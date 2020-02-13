from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, window, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType

tweet_datetime_format = 'EEE MMM dd HH:mm:ss ZZZZ yyyy'

# the schema to parse a tweet in JSON format; we only need two columns
schema = StructType([StructField('created_at', StringType(), True),
                     StructField('text', StringType(), True)])

# launch a Spark session
spark = SparkSession.builder.appName('Packt').getOrCreate()

# get the raw data from a local socket
raw_stream = spark.readStream.format('socket').option('host', 'localhost').option('port', 1234).load()

# parse the json to get separate fields
tweet_stream = raw_stream.select(from_json('value', schema).alias('tweet'))

# create a timestamp by parsing the created_at field
timed_stream = tweet_stream.select(
    to_timestamp('tweet.created_at', tweet_datetime_format).alias('timestamp'),
    'tweet.text')

# To display the tweets without windowing:
# query = lines5.writeStream.outputMode('append').format('console').start()

# create a sliding window of 1 minute with a slide of 10 seconds, with a 'slack time' of 2 seconds
windowed = timed_stream \
    .withWatermark('timestamp', '2 seconds') \
    .groupBy(window('timestamp', '1 minute', '10 seconds'))

# count the tweets per window
counts_per_window = windowed.count().orderBy('window')

# output the windows and counts to the console
query = counts_per_window.writeStream.outputMode('complete').format('console').option("truncate", False).start()
query.awaitTermination()
