from pyspark.sql import SparkSession
from pyspark.sql.functions import col, asc

spark = SparkSession.builder.appName("Packt").getOrCreate()

data = spark.read.csv('../../Datasets/short_netflix_titles.csv', header='true')
# data.show()

movies = data.filter(col("type") == "Movie")

movies.show()
