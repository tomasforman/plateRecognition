import boto3
from botocore.exceptions import NoCredentialsError
from boto3.s3.transfer import S3Transfer

ACCESS_KEY = 'AKIAIPYFKXX53CQGQQIA'
SECRET_KEY = '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'
BUCKET = 'prs-plates'

s3 = S3Transfer(
    boto3.client('s3', aws_access_key_id=ACCESS_KEY, region_name='us-east-1', aws_secret_access_key=SECRET_KEY))


def upload_to_s3(filename):
    try:
        s3.upload_file(filename, BUCKET, filename, extra_args={'ACL': 'public-read'})
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
