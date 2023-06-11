from fastapi import (BackgroundTasks,UploadFile,File,Form,Depends,HTTPException,status)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from models import User
import jwt


# Email_Documentation Link : https://pypi.org/project/fastapi-mail/
# JWT Doc Link :  https://pypi.org/project/PyJWT/
config_credentials = dotenv_values('.env')


conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials['EMAIL'],
    MAIL_PASSWORD = config_credentials['PASS'],
    MAIL_FROM = config_credentials['EMAIL'],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    
)


class EmailSchema(BaseModel):
    email : List[EmailStr]

async def send_email(email: List, instance: User):

    token_data = {
        'id': instance.id,
        'username' : instance.username
    }

    token = jwt.encode(token_data,config_credentials['SECRET'], algorithm=['HS256'])
    
    template = f"""
        <! DOCTYPE html>
        <html>
            <head>

            </head>
            <body>
                <div style = 'display: flex; align-items: center; justify-content:
                center; flex-direction:column'>

                    <h3> Account Verification </h3>
                    <br>
                    <p> Thanks for selecting Our Shops, Please tab below button to verify</p>

                    <a style = 'margin-top: lrem; padding:lrem; border-radius:0.5rem;
                    font-size :lrem; text-decoration:none; background: #0275d8; color: white;'
                    href = "http://localhost:8000/verification/?token{token}"> 
                    Verify your email
                    </a>

                    <p> Please Kindly ignore these email if you not register. Thanks</p>
                </div>
            </body>
        </html>
    """

    message = MessageSchema(
        subject = "OurShop Account Verfication",
        recipients= email,            # List of email
        body = template,
        subtype= 'html', 

    )

    fm = FastMail(conf)
    await fm.send_message(message=message)