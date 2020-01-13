#!/bin/bash

# exit immediately if a command exits with a non-zero exit status
set -e

# 1. chech if there is any data
aws s3 ls

# 2. create your 1st S3 bucket
aws s3api create-bucket --bucket ch10-data

# 3. check s3 buckets again
aws s3 ls

# 4. upload local file to s3 bucket
aws s3 cp ./Data/New_York_City_Leading_Causes_of_Death.csv s3://ch10-data/

# check file
aws s3 ls s3://ch10-data/
