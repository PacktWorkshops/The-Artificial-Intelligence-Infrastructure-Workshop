import os
import boto3
import shutil
from moto import mock_s3


@mock_s3
def test_s3():
    s3_resource = boto3.resource('s3')

    # create a bucket
    s3_resource.create_bucket(Bucket='TEST_BUCKET')

    # write file to a bucket
    try:
        with open('tmp/New_York_City_Leading_Causes_of_Death.csv', 'w') as fout:
            fout.write('foo\n')
    except FileNotFoundError:
        os.mkdir('tmp')
        with open('tmp/New_York_City_Leading_Causes_of_Death.csv', 'w') as fout:
            fout.write('foo\n')

    s3_resource.Object('TEST_BUCKET', 'New_York_City_Leading_Causes_of_Death.csv').put(Body=open('tmp/New_York_City_Leading_Causes_of_Death.csv', 'rb'))

    # download
    s3_resource.Bucket('TEST_BUCKET').download_file(
        'New_York_City_Leading_Causes_of_Death.csv', 
        './tmp/COPY_New_York_City_Leading_Causes_of_Death.csv')
 
    # test
    with open('tmp/COPY_New_York_City_Leading_Causes_of_Death.csv', 'r') as fin:
        assert fin.read() == 'foo\n'

    # clean up
    shutil.rmtree('tmp')