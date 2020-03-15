# 2
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, window, to_timestamp, explode, split, col
from pyspark.sql.types import StructType, StructField, StringType

tweet_datetime_format = 'EEE MMM dd HH:mm:ss ZZZZ yyyy'

schema = StructType([StructField('created_at', StringType(), True),
                     StructField('text', StringType(), True)])

spark = SparkSession.builder.appName('Packt').getOrCreate()
# 3
raw_stream = spark.readStream.format('socket').option('host', 'localhost').option('port', 1234).load()
# 4
tweet_stream = raw_stream.select(from_json('value', schema).alias('tweet'))
# 5
timed_stream = tweet_stream.select(
    to_timestamp('tweet.created_at', tweet_datetime_format).alias('timestamp'),
    # 6
    explode(
        split('tweet.text', ' ')
    ).alias('word'))
# 7 and 8
windowed = timed_stream \
    .withWatermark('timestamp', '1 minute') \
    .groupBy(window('timestamp', '10 minutes'), 'word')

# 9: count the words per window
counts_per_window = windowed.count().orderBy(['window', 'count'], ascending=[0, 1])

# 10: output the windows and counts to the console
query = counts_per_window.writeStream.outputMode('complete').format('console').option("truncate", False).start()
query.awaitTermination()
