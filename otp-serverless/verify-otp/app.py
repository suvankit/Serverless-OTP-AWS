import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DB_TABLE'])

def lambda_handler(event, context):
    body = json.loads(event['body'])

    if 'sessionId' not in body or 'token' not in body:
        return {
            'statusCode': 422,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Required fields not found.',
                'error': 'token and sessionId required'
            })
        }

    data = fetch_session_data(f"{body['sessionId']}_{body['token']}")

    try:
        if data and data[0]['expiryAt'] > int(datetime.now().timestamp()):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Validated'
                })
            }
        else:
            return {
                'statusCode': 422,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Cannot validate OTP.'
                })
            }
    except Exception as err:
        print(err)
        return {
            'statusCode': 422,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Cannot validate OTP.'
            })
        }

def fetch_session_data(pk):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('pk').eq(pk)
    )
    return response['Items']

