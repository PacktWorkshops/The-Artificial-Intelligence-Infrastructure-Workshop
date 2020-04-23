#!/bin/bash

# exit immediately if a command exits with a non-zero exit status
set -e

# 1. create your 1st S3 bucket
aws s3api create-bucket --acl private --bucket ${BACKUP_BUCKET} --region us-east-1

# 2. check s3 buckets again
aws s3 ls

# 3. copy file to backup
aws s3 cp s3://${BUCKET_NAME}/New_York_City_Leading_Causes_of_Death.csv s3://${BACKUP_BUCKET}/

# 4. check file
aws s3 ls s3://${BACKUP_BUCKET}/
