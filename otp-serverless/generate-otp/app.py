import os
import random
import string
import json
from email_validator import validate_email, EmailNotValidError
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DB_TABLE'])

otp_expiry_time = int(os.environ['OTP_EXPIRY_MINUTES'])
token_length = int(os.environ['TOKEN_LENGTH'])

def lambda_handler(event, context):
    body = json.loads(event['body'])

    try:
        validate_email(body['email'])
    except EmailNotValidError as e:
        return {
            'statusCode': 422,
            'body': json.dumps({
                'message': 'Required field email not found or invalid'
            })
        }

    session_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    otp = ''.join(random.choices(string.digits, k=token_length))

    item = {
        'pk': f"{session_token}_{otp}",
        'email': body['email'],
        'expiryAt': int(os.time.time()) + otp_expiry_time * 60
    }

    try:
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'OTP generated',
                'data': {
                    'token': session_token
                }
            })
        }
    except Exception as e:
        print(f"Error: {e.stack}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'OTP generation failed',
                'error': str(e)
            })
        }

