import json
import boto3
import os

def lambda_handler(event, context): 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get("TABLENAME"))

    body =json.loads(event["Records"][0]["body"])
    message = json.loads(body["Message"])

    table.put_item(
        Item={
            'orderid': message['order']['orderid'],
            'coffeetype': message['order']['coffeetype'],
            'coffeesize': message['order']["coffeesize"],
            'vendorid': message['order']["vendorid"]
        })
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps("Order Placed")
    } 
