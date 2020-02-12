#!/bin/bash

# exit immediately if a command exits with a non-zero exit status
set -e

# 1. change your working dir to Data
cd Data/

# 2. remove the file
rm ch10-data/New_York_City_Leading_Causes_of_Death.csv

# 3. download file from s3
aws s3 cp s3://ch10-data/New_York_City_Leading_Causes_of_Death.csv ./

# 4. check file
ls