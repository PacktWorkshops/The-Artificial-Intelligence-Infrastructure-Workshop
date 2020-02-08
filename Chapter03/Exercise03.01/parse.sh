head ../../Datsets/netflix_titles.csv | gawk -f netflix_console.awk

cat ../../Datsets/netflix_titles.csv | gawk -f netflix.awk > netflix_filtered.csv
