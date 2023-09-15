import boto3
from pathlib import Path

bucket='torq-dataproducts-etl-data-lake'
remote_folder='datasets/export'
local_folder = Path('import')

bucket = boto3.resource('s3').Bucket(bucket)

for obj in bucket.objects.filter(Prefix=remote_folder):
    print(obj.key)
    if '.csv' in obj.key:
        bucket.download_file(obj.key, local_folder / obj.key.split('/')[-1])