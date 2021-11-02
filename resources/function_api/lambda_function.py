import json, boto3, os, logging
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all(['boto3','botocore'])

sns = boto3.client('sns')

@xray_recorder.capture('lambda_api')
def lambda_handler(event, context): 
    with xray_recorder.in_subsegment('metadata') as subsegment:
        subsegment.put_metadata("RequestID", context.aws_request_id)

    return publish_message(event)

@xray_recorder.capture()
def publish_message(event):
    body = event["body"]
    topic = os.environ.get('TOPIC')
    accountid = json.loads(body)['order']['accountid']
    vendorid = json.loads(body)['order']['vendorid']
    
    with xray_recorder.in_subsegment('annotations') as subsegment:
        subsegment.put_annotation("accountid", accountid)
        subsegment.put_annotation("vendorid", vendorid)

    try:
        response = sns.publish(
            TopicArn=topic,
            Message=body,
            MessageAttributes={
                'accountid': {
                    'StringValue': accountid,
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