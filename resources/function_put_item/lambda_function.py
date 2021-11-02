import boto3, json, logging, os
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all(['boto3'])

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLENAME'))

@xray_recorder.capture('put_item_dynamodb')
def lambda_handler(event, context):
    return put_item(event)

def put_item(event): 
    body =json.loads(event["Records"][0]["body"])
    message = json.loads(body["Message"])

    try:
        table.put_item(
            Item={
                'accountid': message['order']['accountid'],
                'vendorid': message['order']["vendorid"],
                'orderdate':message['order']["orderdate"],
                'city':message['order']["city"],
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