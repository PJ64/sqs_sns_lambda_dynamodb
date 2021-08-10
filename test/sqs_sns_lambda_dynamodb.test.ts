import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as SqsSnsLambdaDynamodb from '../lib/sqs_sns_lambda_dynamodb-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new SqsSnsLambdaDynamodb.SqsSnsLambdaDynamodbStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
