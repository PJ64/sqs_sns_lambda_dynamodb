## Example
This is a basic CDK TypeScript example that deploys AWS Lambda functions decoupled by Amazon SNS and Amazon SQS. The example also demonstates using Python to put items to Amazon DynamoDB, put object to Amazon S3 and using Amazon SNS message attributes. 

The first Lambda function integrates with Amazon API Gateway. Messages that are sent to the API Gateway are published using Amazon SNS by fanning out the messages to Amazon SQS queues. The Lambda functions that are associated with the queues process the messages when they are recieved.

The invoice Lambda function writes the message to an Amazon S3 bucket, this is saved as an object. The order Lambda function writes messages to a Amazon DynamoDB table this is saved as an item. The Amazon DynamoDB table is partitioned on an accountid attribute and also includes a sort key on the vendorid attribute, together they form the primary key.

Additional Lambda functions are deployed to get the order item from Amazon DyanmoDB and the object from the Amazon S3 bucket.

![architecture](./images/architecture_1.png "Architecture")

**Jupyter Notebook Scripts**

1. The first script posts new orders to the API Gateway. The order is written to an Amazon DyanmoDB table and invoice is written to an Amazon S3 bucket.

2. The second script creates a json formatter which is used to render the json output in a readable format.

3. The fourth script is used to query items in the Amazon DynamoDB table

4. The final script is used to generate a pre-signed url used to get the object from the S3 bucket.

## Setup

1. The following prerequisities are required for this example
  
```bash
npm install -g typescript
npm install -g aws-cdk
```
Install Jupyter Notebook following instructions on this ['site'](https://jupyter.org/install).

2. Since this CDK project uses ['Assests'](https://docs.aws.amazon.com/cdk/latest/guide/assets.html), you might need to run the following command to provision resources the AWS CDK will need to perform the deployment.

```bash 
cdk bootstrap
```

2. Install the dependencies

```bash
npm install
```

3. Execute **cdk synth** to synthesize as AWS CloudFormation template

```bash
cdk synth
```

4. Execute **cdk deploy** to deploy the template and build the stack

```bash
cdk deploy
```

1. Open the Jupyter Notebook in the **jupyter_notebook directory** follow the instructions.

2. Check the dynamoDB table and S3 bucket