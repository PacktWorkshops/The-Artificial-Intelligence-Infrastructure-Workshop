#!/bin/bash

# exit immediately if a command exits with a non-zero exit status
set -e

# 1. create your 1st S3 bucket
aws s3api create-bucket --acl private --bucket storage-for-ai-data-backup

# 2. check s3 buckets again
aws s3 ls

# 3. copy file to backup
aws s3 cp s3://ch10-data/New_York_City_Leading_Causes_of_Death.csv s3://storage-for-ai-data-backup/

# 4. check file
aws s3 ls s3://storage-for-ai-data-backup/

2020-01-13 21:20:11      91294 New_York_City_Leading_Causes_of_Death.csv