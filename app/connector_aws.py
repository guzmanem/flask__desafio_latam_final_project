import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
BUCKET_NAME = 'edgarguzman' 
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
for s3_file in your_bucket.objects.all():
    print(s3_file.key)

s3.Bucket('edgarguzman').upload_file("test.txt", "test/test.txt")