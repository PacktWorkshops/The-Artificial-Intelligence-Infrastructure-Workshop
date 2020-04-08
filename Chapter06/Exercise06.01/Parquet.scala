// Read CSV
var df_census_csv = spark.read.options(Map("inferSchema"->"true","delimiter"->",","header"->"true")).csv("F:/Chapter06/Data/Census.csv")

// Read JSON
var df_census_json = spark.read.json("F:/Chapter06/Data/Census.json")

// Show the df
df_census_csv.show()
df_census_json.show()


// Writing to PARQUET

// Using CSV Data frame
df_census_csv.write.parquet("F:/Chapter06/Data/Output/census_csv.parquet")

// Using JSON Data frame
df_census_json.write.parquet("F:/Chapter06/Data/Output/census_json.parquet")


// Reading PARQUET file

val df_census_parquet = spark.read.parquet("F:/Chapter06/Data/Output/census_csv.parquet")
df_census_parquet.show()