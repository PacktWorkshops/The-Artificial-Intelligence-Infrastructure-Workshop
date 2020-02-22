head ../../Datasets/netflix_titles_nov_2019.csv | gawk -f netflix_console.awk

cat ../../Datasets/netflix_titles_nov_2019.csv| gawk -f netflix.awk > netflix_filtered.csv
