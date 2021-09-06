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
                'accountid': message['order']['accountid'],
                'vendorid': message['order']["vendorid"],
                'orderdate':message['order']["orderdate"],
                'details':{
                    'coffeetype': message['order']['details']['coffeetype'],
                    'coffeesize': message['order']['details']["coffeesize"],
                    'unitprice': message['order']['details']["unitprice"],
                    'quantity': message['order']['details']["quantity"]
                },
            })
        logger.info("PutItem %s to table %s.",message,table)
    except ClientError:
        logger.exception("Couldn't PutItem %s to table %s",message,table)
        raise