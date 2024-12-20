import os
import boto3

aws_ses = boto3.client('ses')

from_address = os.environ['FROM_ADDRESS']

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            pk = record['dynamodb']['NewImage']['pk']['S'].split('_')
            otp = pk[1]
            to_address = record['dynamodb']['NewImage']['email']['S']
            send_email(otp, to_address)

async def send_email(otp, to_address):
    html_body = f"""
    <!DOCTYPE html>
    <html>
      <body>
        <p>Use this code to verify your login at Simple OTP</p>
        <p><h1>{otp}</h1></p>
      </body>
    </html>
    """

    params = {
        'Destination': {
            'ToAddresses': [to_address]
        },
        'Message': {
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': html_body
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Your OTP at Simple OTP'
            }
        },
        'Source': f'SimpleOTP <{from_address}>'
    }

    await aws_ses.send_email(params)

