import boto3
import json
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
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