import os
import json
import boto3
import shutil
import pandas as pd

if __name__ == "__main__":

    # set your bucket name here
    # 'ch10-data' is NOT your bucket. It's just an example here
    # you should replace your bucket below
    BUCKET_NAME = 'ch10-data'

    # 1. download data from S3 bucket
    s3_resource = boto3.resource('s3')
    try:
        s3_resource.Bucket(BUCKET_NAME).download_file(
            'New_York_City_Leading_Causes_of_Death.csv', 
            './tmp/New_York_City_Leading_Causes_of_Death.csv')
    except FileNotFoundError:
        os.mkdir('tmp/')
        s3_resource.Bucket(BUCKET_NAME).download_file(
            'New_York_City_Leading_Causes_of_Death.csv', 
            './tmp/New_York_City_Leading_Causes_of_Death.csv')
        
    # read data
    df_data = pd.read_csv('tmp/New_York_City_Leading_Causes_of_Death.csv')

    # 2. replace "." with value 0 & and convert to float type
    df_data_cleaned = df_data.replace('.', 0).astype({'Deaths': float})

    # 3. get top 3 death causes for each ethnicity
    top_causes = {}
    for ethnicity, df_g in df_data_cleaned.groupby(['Race Ethnicity']):
        df_top_3_causes = df_g.groupby('Leading Cause')[['Deaths']].sum().sort_values('Deaths', ascending=False).head(3)
        top_3_causes = df_top_3_causes.index.values.tolist()
        top_causes.update({ethnicity: top_3_causes})

    # 4. dump output data to a JSON file
    with open('tmp/top_causes_per_ethnicity.json', 'w') as fout:
        json.dump(top_causes, fout)

    # 5. upload data to S3
    s3_resource.Bucket(BUCKET_NAME).upload_file(
        'tmp/top_causes_per_ethnicity.json',
        'top_causes_per_ethnicity.json')

    # clean up tmp
    shutil.rmtree('./tmp')
