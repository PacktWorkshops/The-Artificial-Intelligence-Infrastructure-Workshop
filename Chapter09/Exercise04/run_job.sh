#!/bin/bash

set -e

# set config
DATE=17.14.11
SOURCE_FILE=../Data/USvideos.csv.zip
CAT_FILE=../Data/US_category_id.json
OUTPUT_FILE=../Data/top_10_trendy_cats.csv
SRC_DIR=../Exercise03

echo "[[ JOB ]] runs on date $DATE with file located in $SOURCE_FILE and meta data located in $CAT_FILE"
echo "[[ JOB ]] result data will be persisted in $OUTPUT_FILE"

# run job
echo "[[ RUNNING JOB ]] step 1: filter source data"
python $SRC_DIR/filter_data.py --file $SOURCE_FILE --date $DATE

echo "[[ RUNNING JOB ]] step 1.1: preprcess meta data"
python $SRC_DIR/preprocess_data.py --file $CAT_FILE

echo "[[ RUNNING JOB ]] step 2: join data"
python $SRC_DIR/join_data.py

echo "[[ RUNNING JOB ]] step 3: rank categories"
python $SRC_DIR/sort_data.py

echo "[[ RUNNING JOB ]] step 4: persist result data"
python $SRC_DIR/store_data.py --path $OUTPUT_FILE

if [ "$?" = "0" ]; then
	echo "[[ JOB ]] END"
else
	echo "[[ JOB FAILS!! ]]" 1>&2
	exit 1
fi