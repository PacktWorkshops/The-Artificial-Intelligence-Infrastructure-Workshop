// Read CSV
var df_census_csv = spark.read.options(Map("inferSchema"->"true","delimiter"->",","header"->"true")).csv("F:/Chapter06/Data/Census.csv")

// Read JSON
var df_census_json = spark.read.json("F:/Chapter06/Data/Census.json")

// Show the df
df_census_csv.show()
df_census_json.show()


//  Writing to ORC

// Using CSV Data frame
df_census_csv.write.orc("F:/Chapter06/Data/Output/census_csv.orc")

// Using JSON Data frame
df_census_json.write.orc("F:/Chapter06/Output/Data/census_json.orc")


// Reading ORC file
val df_census_orc = spark.read.orc("F:/Chapter06/Data/Output/census_csv.orc")
df_census_orc.show()
