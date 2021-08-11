import boto3,json,os

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    
    body =json.loads(event["Records"][0]["body"])
    message = json.dumps(body["Message"])
    encoded_string = message.encode("utf-8")

    bucket = s3.Bucket(os.environ.get('BUCKETNAME'))
    path = 'order.json'
    data = encoded_string
    bucket.put_object(
        ContentType='application/json',
        Key=path,
        Body=data,
    )