## Example
This example is designed for a concept mobile application called Skip the Line, which allows user to pre-order takeaway coffee while they are in transit. Just as the train pulls into the station, the user can order a coffee and pick it up on the way past the coffee shop.

Asynchronous communication is considered to be a best practice when building modern internet scale applications. By decoupling components, you enable those components to scale independently. In this example the Lambda functions communicates asynchronously using a SNS Topic and SQS Queue. This architecture allows the functions to scale out to produce or process events independently without impacting each other. In this particular design an order and invoice can be processed in parallel without any issues of one function being faster and completing before the other. By integrating an API Gateway with Lambda, SNS, SQS and an Amazon DynamoDB table you can build an architecture that is scalable, highly available and cost effective. 

There are two Lambda layers included in the example. The X-Ray layer is used to instrument the Python code in the Lambda functions and the second layer has the CloudWatch Lambda insight extensions. By including these monitoring tools and logging, you have end to end observability of the distributed architecture.

The Amazon DynamoDB table is partitioned on an accountid attribute and also includes a sort key on the vendorid attribute, together they form the primary key. The combination of these keys ensures that customer can only have one active order for each vendor. After the order is processed the item would be removed from the table, similar behaviour to a shopping cart.


![architecture](./images/architecture_2.png "Architecture")

## Setup

You will need to download and install [Node.js](https://nodejs.org/en/download/) before you can start using the AWS Cloud Development Kit.

This example is developed using the AWS CDK and Typescript, so you will need to install both Typescript and the CDK using the following commands
```
npm install -g typescript
npm install -g aws-cdk@latest
```
Since this CDK project uses ['Assests'](https://docs.aws.amazon.com/cdk/latest/guide/assets.html), you might need to run the following command to provision resources the AWS CDK will need to perform the deployment.

```bash 
cdk bootstrap
```

The testing scripts can be executed using Jupyter Notebook. There are a few methods for installing Jupyter Notebooks. These instructions will help you get to started with [JupyterLab](https://jupyter.org/install) installation. 

You can also install Jupyter Notebooks as part of [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installation.

To download this example, you will need to install [Git](https://github.com/git-guides/install-git). After installing git follow these [instructions](https://github.com/git-guides/git-clone) to learn how to clone the repository.

After the repository has been cloned set the command prompt path to the cloned directory and run the following command to install the project dependencies.

```bash
npm install
```

**cdk synth** executes the application which translates the Typescript code into an AWS CloudFormation template.

```bash
cdk synth
```

After the synth command has generated the template use the  **cdk deploy** command to deploy the template to AWS CloudFormation and build the stack. You will be prompted to confirm the deployment with y/n.

```bash
cdk deploy
```
## Test the Stack
We need to install Jest since we are using the Jest framework to test the stack. Testing the stack is optional.
```
npm install --save-dev jest @types/jest @aws-cdk/assert
```

## Run the Example
Open the Jupyter Notebook in the **jupyter_notebook directory** follow the instructions.

## Cleanup
From the command prompt execute the following command: **cdk destroy**

## Deployed Resources
|	Identifier	|	Service	|	Type	|
|	:---	|	:---	|	:---	|
|	SqsSnsLambdaDynamodbStack-CustomS3AutoDeleteObject-<id>	|	Lambda	|	Function	|
|	SqsSnsLambdaDynamodbStack-CustomS3AutoDeleteObject-<id>	|	IAM	|	Role	|
|	sqs_sns_lambda_dynamodb	|	DynamoDB	|	Table	|
|	sqs_sns_lambda_dynamodb_get_item	|	Lambda	|	Function	|
|	get_presigned_url	|	Lambda	|	Function	|
|	account/SqsSns-Order-<id>	|	ApiGateway	|	Account	|
|	SqsSnsLambdaDynamodbStack-OrderApiCloudWatchRoleB1-<id>	|	IAM	|	Role	|
|	restapis/<id>	|	ApiGateway	|	RestApi	|
|	<bucketname>	|	S3	|	Bucket	|
|	sqs_sns_lambda_dynamodb_api	|	Lambda	|	Function	|
|	sqs_sns_lambda_dynamodb_put_item	|	Lambda	|	Function	|
|	<id>	|	Lambda	|	EventSourceMapping	|
|	sqs_sns_lambda_dynamodb_put_object	|	Lambda	|	Function	|
|	<id>	|	Lambda	|	EventSourceMapping	|
|	lambda_api_topic	|	SNS	|	Topic	|
|	put_item_queue	|	SQS	|	Queue	|
|	put_object_queue	|	SQS	|	Queue	|
|	sqs_sns_lambda_dynamodb_get_item	|	IAM	|	Role	|
|	sqs_sns_lambda_dynamodb_get_object	|	IAM	|	Role	|
|	sqs_sns_lambda_dynamodb_api	|	IAM	|	Role	|
|	sqs_sns_lambda_dynamodb_put_item	|	IAM	|	Role	|
|	sqs_sns_lambda_dynamodb_put_object	|	IAM	|	Role	|
|	xray_sdk:1	|	Lambda	|	LayerVersion	|
