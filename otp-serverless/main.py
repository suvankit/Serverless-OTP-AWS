# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random
import string
import boto3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('OTP_TABLE')

# SES setup
ses_client = boto3.client('ses')

# Helper functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def send_email(email, otp):
    try:
        response = ses_client.send_email(
            Source='sender@example.com',
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': 'Your OTP'
                },
                'Body': {
                    'Text': {
                        'Data': f'Your OTP is: {otp}'
                    }
                }
            }
        )
    except Exception as e:
        print(e)
    else:
        print('Email sent! Message ID:'),
        print(response['MessageId'])

# Routes
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Hardcoded credentials for now
    valid_email = "user@example.com"
    valid_password = "password"

    if email == valid_email and password == valid_password:
        otp = generate_otp()
        session_id = generate_session_id()

        # Save OTP and session ID to DynamoDB 
        table.put_item(
            Item={
                'session_id': session_id,
                'otp': otp
            }
        )

        # Send email with OTP
        send_email(email, otp)

        return templates.TemplateResponse("otp.html", {"request": request, "session_id": session_id})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})

@app.post("/verify")
async def verify_otp(request: Request, session_id: str = Form(...), otp: str = Form(...)):
    # Retrieve OTP from DynamoDB
    response = table.get_item(
        Key={
            'session_id': session_id
        }
    )

    if 'Item' in response:
        stored_otp = response['Item']['otp']

        if otp == stored_otp:
            # OTP is valid
            return templates.TemplateResponse("success.html", {"request": request})
        else:
            # OTP is invalid
            return templates.TemplateResponse("otp.html", {"request": request, "session_id": session_id, "error": "Invalid OTP"})
    else:
        # Session ID not found
        return templates.TemplateResponse("error.html", {"request": request, "error": "Session ID not found"})