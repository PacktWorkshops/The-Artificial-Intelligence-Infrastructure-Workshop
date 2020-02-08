head netflix_titles.csv | gawk -f netflix_console.awk

cat netflix_titles.csv | gawk -f netflix.awk > netflix_filtered.csv
