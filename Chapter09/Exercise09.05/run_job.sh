#!/bin/bash

# set -e

# set config
DATE=17.14.11
SOURCE_FILE=../Data/USvideos.csv.zip
CAT_FILE=../Data/US_category_id.json
OUTPUT_FILE=../Data/top_10_trendy_cats.csv
SRC_DIR=../Exercise09.03

echo "[[ JOB ]] runs on date $DATE with file located in $SOURCE_FILE and metadata located in $CAT_FILE"
echo "[[ JOB ]] result data will be persisted in $OUTPUT_FILE"

# run job
echo "[[ RUNNING JOB ]] step 1: filter source data"
python $SRC_DIR/filter_data.py --file $SOURCE_FILE --date $DATE &

echo "[[ RUNNING JOB ]] step 1.1: preprcess metadata"
python $SRC_DIR/preprocess_data.py --file $CAT_FILE &

echo "[[ BLOCKING JOB ]] additional step: check cached files and trigger next step"
while [ ! -f ./tmp/data_cats.csv ] || [ ! -f ./tmp/data_vids.csv ]
do
  sleep 1
done

echo "[[ RUNNING JOB ]] step 2: join data"
python $SRC_DIR/join_data.py

echo "[[ RUNNING JOB ]] step 3: rank categories"
python $SRC_DIR/sort_data.py

echo "[[ RUNNING JOB ]] step 4: persist result data"
python $SRC_DIR/store_data.py --path $OUTPUT_FILE

if [ "$?" = "0" ]; then
	rm -rf ./tmp/
	echo "[[ JOB ]] END"
else
	rm -rf ./tmp/
	echo "[[ JOB FAILS!! ]]" 1>&2
	exit 1
fi
