import { Topic } from '@aws-cdk/aws-sns';
import { SqsSubscription } from '@aws-cdk/aws-sns-subscriptions';
import { Queue } from '@aws-cdk/aws-sqs';
import { LambdaIntegration, RestApi, Cors} from '@aws-cdk/aws-apigateway';
import { AttributeType, Table } from '@aws-cdk/aws-dynamodb';
import { Runtime, Code, Function } from '@aws-cdk/aws-lambda';
import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources'
import { Role, ServicePrincipal, ManagedPolicy, PolicyStatement } from '@aws-cdk/aws-iam';
import { Bucket } from '@aws-cdk/aws-s3';
import * as cdk from '@aws-cdk/core';


export class SqsSnsLambdaDynamodbStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //create sqs queues
    const put_object_queue = new Queue(this, "put_object_queue",{
      queueName: "put_object_queue"
    })

    const put_item_queue = new Queue(this, "put_item_queue",{
      queueName: "put_item_queue"      
    })

    //create sns topic
    const lambda_api_topic = new Topic(this, "lambda_api_topic",{
      topicName: "lambda_api_topic",
      displayName: "lambda_api_topic"
    })

    lambda_api_topic.addSubscription(new SqsSubscription(put_object_queue))
    lambda_api_topic.addSubscription(new SqsSubscription(put_item_queue))

    //Create DynamoDB table
    const dynamoTable = new Table(this, "DynamoDBTable",{
      partitionKey: {
        name: 'accountid',
        type: AttributeType.STRING
      },
      sortKey: {
        name: 'vendorid',
        type: AttributeType.STRING
      },
      tableName: 'sqs_sns_lambda_dynamodb',
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    
    //Create S3 bucket
    const bucket = new Bucket(this, "S3Bucket",{
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true
    })

    //Create IAM roles
    const role_put_object = new Role(this, "role_put_object",{
        assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
        roleName: "sqs_sns_lambda_dynamodb_put_object"
    });
    
    const role_get_object = new Role(this, "role_get_object",{
      assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
      roleName: "sqs_sns_lambda_dynamodb_get_object"
    });

    const role_put_item = new Role(this, "role_put_item",{
      assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
      roleName: "sqs_sns_lambda_dynamodb_put_item"
    });

    const role_get_item = new Role(this, "role_get_item",{
      assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
      roleName: "sqs_sns_lambda_dynamodb_get_item"
  });

    const role_lambda_api = new Role(this, "role_lambda_api",{
      assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
      roleName: "sqs_sns_lambda_dynamodb_api"
    });

    //Setup role permissions
    role_put_object.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    role_put_item.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    role_lambda_api.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    role_get_object.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));
    role_get_item.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole"));

    role_put_object.addToPolicy(new PolicyStatement({
      resources: [bucket.bucketArn, bucket.bucketArn + "/*"],
      actions: ['s3:PutObject'],
    }));
    
    role_put_item.addToPolicy(new PolicyStatement({
      resources: [dynamoTable.tableArn],
      actions: ['dynamodb:PutItem'],
    }));

    role_lambda_api.addToPolicy(new PolicyStatement({
      resources: [lambda_api_topic.topicArn],
      actions: ['sns:Publish'],
    }));

    role_get_object.addToPolicy(new PolicyStatement({
      resources: [bucket.bucketArn, bucket.bucketArn + "/*"],
      actions: ['s3:GetObject'],
    }));
    
    role_get_item.addToPolicy(new PolicyStatement({
      resources: [dynamoTable.tableArn],
      actions: ['dynamodb:GetItem'],
    }));

    //Create Lambda functions. One for read and one for writing
    const function_put_item = new Function(this, "function_put_item",{
      runtime: Runtime.PYTHON_3_7,
      handler: "lambda_handler.lambda_handler",
      code: Code.fromAsset("resources/function_put_item"),
      functionName: "sqs_sns_lambda_dynamodb_put_item",
      role: role_put_item,
      environment: {
        'TABLENAME': dynamoTable.tableName
      }
    });
    
    const function_put_object = new Function(this, "function_put_object",{
      runtime: Runtime.PYTHON_3_7,
      handler: "lambda_handler.lambda_handler",
      code: Code.fromAsset("resources/function_put_object"),
      functionName: "sqs_sns_lambda_dynamodb_put_object",
      role: role_put_object,
      environment: {
        'BUCKETNAME': bucket.bucketName
      }
    });

    const lambda_get_presigned_url = new Function(this, "GetUrlLambdaFunction",{
      runtime: Runtime.PYTHON_3_7,
      handler: "lambda_handler.lambda_handler",
      code: Code.fromAsset("resources/function_get_presigned_url"),
      functionName: "get_presigned_url",
      role: role_get_object,
      environment: {
        'BUCKETNAME': bucket.bucketName
      }
    });

    const lambda_get_order_item = new Function(this, "GetLambdaFunction",{
      runtime: Runtime.PYTHON_3_7,
      handler: "lambda_handler.lambda_handler",
      code: Code.fromAsset("resources/function_get_item"),
      functionName: "sqs_sns_lambda_dynamodb_get_item",
      role: role_get_item,
      environment: {
        'TABLENAME': dynamoTable.tableName
      }
    });

    const function_api = new Function(this, "function_api",{
      runtime: Runtime.PYTHON_3_7,
      handler: "lambda_handler.lambda_handler",
      code: Code.fromAsset("resources/function_api"),
      functionName: "sqs_sns_lambda_dynamodb_api",
      role: role_lambda_api,
      environment: {
        'TOPIC': lambda_api_topic.topicArn
      }
    });

    function_put_item.addEventSource(new SqsEventSource(put_item_queue));
    function_put_object.addEventSource(new SqsEventSource(put_object_queue));

    //Create REST Api and integrate the Lambda function
    var api = new RestApi(this, "OrderApi",{
      restApiName: "sqs_sns_lambda_dynamodb",
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: Cors.ALL_METHODS}
    });

    var function_api_integration = new LambdaIntegration(function_api, {
      requestTemplates: {
            ["application/json"]: "{ \"statusCode\": \"200\" }"
        }
    });

    var function_get_object_integration = new LambdaIntegration(lambda_get_presigned_url);
    var function_get_item_integration = new LambdaIntegration(lambda_get_order_item);

    var api_order_resource = api.root.addResource("order");
    api_order_resource.addMethod("POST", function_api_integration);
    api_order_resource.addMethod("GET", function_get_item_integration);

    var api_invoice_resource = api.root.addResource("invoice");
    api_invoice_resource.addMethod("GET", function_get_object_integration);
  }
}