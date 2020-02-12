import os
import boto3
import json
import shutil
from moto import mock_s3


@mock_s3
def test_s3():
    s3_resource = boto3.resource('s3')

    # create a bucket
    s3_resource.create_bucket(Bucket='ch10-data')

    # write file to a bucket
    top_causes = {
        "Asian and Pacific Islander": 
        ["Malignant Neoplasms (Cancer: C00-C97)", "Diseases of Heart (I00-I09, I11, I13, I20-I51)"]
    }
    try:
        with open('tmp/top_causes_per_ethnicity.json', 'w') as fout:
            json.dump(top_causes, fout)
    except FileNotFoundError:
        os.mkdir('tmp')
        with open('tmp/top_causes_per_ethnicity.json', 'w') as fout:
            json.dump(top_causes, fout)

    s3_resource.Object('ch10-data', 'top_causes_per_ethnicity.json').put(Body=open('tmp/top_causes_per_ethnicity.json', 'rb'))

    # download
    s3_resource.Bucket('ch10-data').download_file(
        'top_causes_per_ethnicity.json', 
        'tmp/copy_top_causes_per_ethnicity.json')
 
    # test
    assert json.load(open('tmp/copy_top_causes_per_ethnicity.json')) == top_causes 

    # clean up
    shutil.rmtree('tmp')