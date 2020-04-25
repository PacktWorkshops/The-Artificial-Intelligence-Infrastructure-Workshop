import os
import shutil
import boto3
import pandas as pd

if __name__ == "__main__":

    # set your bucket name here
    # 'ch10-data' is NOT your bucket. It's just an example here
    # you should replace your bucket below
    BUCKET_NAME = 'ch10-data'

    # create s3 resource
    s3_resource = boto3.resource('s3')

    # downfile from bucket
    try:
        s3_resource.Bucket(BUCKET_NAME).download_file(
            'New_York_City_Leading_Causes_of_Death.csv', 
            './tmp/New_York_City_Leading_Causes_of_Death.csv')
    except FileNotFoundError:
        os.mkdir('tmp/')
        s3_resource.Bucket(BUCKET_NAME).download_file(
            'New_York_City_Leading_Causes_of_Death.csv', 
            './tmp/New_York_City_Leading_Causes_of_Death.csv')

    # read file with pandas
    df = pd.read_csv('./tmp/New_York_City_Leading_Causes_of_Death.csv')

    # filter out data with invalid values
    df_filterred = df[df['Deaths'].apply(lambda x: str(x).isdigit())]
    df_filterred['Deaths'] = df_filterred['Deaths'].apply(lambda x: int(x))

    # calculate number of deaths for each year
    df_agg = df_filterred.groupby('Leading Cause')[['Deaths']].sum()

    # sort and take top 10
    df_top10 = df_agg.sort_values('Deaths', ascending=False).head(10)

    # write new data to new file
    df_top10.to_csv('tmp/New_York_City_Top10_Causes.csv')

    # upload data to S3
    s3_resource.Bucket(BUCKET_NAME).upload_file(
        'tmp/New_York_City_Top10_Causes.csv',
        'New_York_City_Top10_Causes.csv')

    # clean up tmp
    shutil.rmtree('./tmp')

    print('[ run_pipeline.py ] Done uploading result data to S3 bucket')
