head netflix_titles_nov_2019.csv | gawk -f netflix.awk

cat netflix_titles_nov_2019.csv| gawk -f netflix.awk > netflix_filtered.csv
