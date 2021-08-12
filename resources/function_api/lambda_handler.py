import json
import boto3
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context): 
    sns = boto3.client('sns')    
    body = event["body"]
    topic = os.environ.get('TOPIC')
    orderid = json.loads(body)['order']['orderid']
    
    try:
        response = sns.publish(
            TopicArn=topic,
            Message=body,
            MessageAttributes={
                'orderid': {
                    'StringValue': orderid,
                    'DataType': 'String'
                    }
            }
        )
        message_id = response['MessageId']
        logger.info("Published message %s to topic %s.", body,topic)

        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": 'application/json',
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,X-Api-Key',
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps(message_id)
        }

    except ClientError:
        logger.exception("Couldn't publish message to %s.", topic)
        raise