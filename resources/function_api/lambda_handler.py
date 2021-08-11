import json
import boto3
import os

def lambda_handler(event, context): 
    body = event["body"]
    sns = boto3.client('sns')    
    response = sns.publish(
        TopicArn=os.environ.get('TOPIC'),
        Message=body
    )

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,X-Api-Key',
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        'body': json.dumps(response)
    }