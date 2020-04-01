from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, size

spark = SparkSession.builder.appName("Packt").getOrCreate()

data = spark.read.csv('../../Datasets/netflix_titles_nov_2019.csv', header='true')
data.show()

# take only the movies
movies = data.filter((col('type') == 'TV Show') & ((col('rating') == 'TV-G') | (col('rating') == 'TV-Y')))
movies.show()

# add a column with the number of actors
transformed = movies.withColumn('count_lists', size(split(movies['listed_in'], ',')))

# select a subset of columns to store
selected = transformed.select('title', 'cast', 'rating', 'release_year', 'duration', 'count_lists', 'listed_in', 'description')
selected.show()

# write the contents of the DataFrame to disk
selected.write.csv('transformed2.csv', header='true')
