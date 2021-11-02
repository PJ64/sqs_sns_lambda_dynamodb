import boto3, json, logging, os
from botocore.exceptions import ClientError

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all(['boto3'])

s3 = boto3.resource('s3')

@xray_recorder.capture('put_object_s3')
def lambda_handler(event, context):
    put_object(event)

def put_object(event):
    bucket = s3.Bucket(os.environ.get('BUCKETNAME'))
    
    body =json.loads(event["Records"][0]["body"])
    accountid = body["MessageAttributes"]["accountid"]["Value"]        
    message = json.dumps(body["Message"])
    data = message.encode("utf-8")
    path = 'accountid_' + accountid + '.json'

    try:
        bucket.put_object(
            ContentType='application/json',
            Key=path,
            Body=data,
        )
        logger.info("PutObject to bucket %s.",bucket)
    except ClientError:
        logger.exception("Couldn't PutObject to bucket %s.",bucket)
        raise