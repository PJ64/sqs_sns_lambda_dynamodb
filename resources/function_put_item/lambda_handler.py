import json
import boto3
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context): 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("TABLENAME"))

    body =json.loads(event["Records"][0]["body"])
    message = json.loads(body["Message"])

    try:
        table.put_item(
            Item={
                'orderid': message['order']['orderid'],
                'coffeetype': message['order']['coffeetype'],
                'coffeesize': message['order']["coffeesize"],
                'vendorid': message['order']["vendorid"]
            })
        logger.info("PutItem %s to table %s.",body,table)
    except ClientError:
        logger.exception("Couldn't PutItem %s to table %s",body,table)
        raise