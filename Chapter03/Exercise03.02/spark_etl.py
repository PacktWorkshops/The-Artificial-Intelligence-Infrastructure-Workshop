from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, size

spark = SparkSession.builder.appName("Packt").getOrCreate()

data = spark.read.csv('../../Datasets/netflix_titles_nov_2019.csv', header='true')
# data.show()

# take only the movies
movies = data.filter((col('type') == 'Movie') & (col('release_year') == 2019))
# movies.show()

# add a column with the number of actors
transformed = movies.withColumn('count_cast', size(split(movies['cast'], ',')))

# select a subset of columns to store
selected = transformed.select('title', 'director', 'count_cast', 'cast', 'rating', 'release_year', 'type')
selected.show()

# write the contents of the DataFrame to disk
selected.write.csv('transformed.csv', header='true')
