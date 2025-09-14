from smtplib import SMTP_PORT
from utility.authentication import verify_token
from utility.log_to_file import log_to_file

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import status, HTTPException, APIRouter
from schemas.schemas import Token, TruckNoti
import os
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Form, Depends
from typing import Annotated
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

load_dotenv()

router = APIRouter(
    tags=['Notifications'],
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
RECEIVER_EMAIL_ADDRESS = os.getenv("RECEIVER_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
API_TOKEN = os.getenv("TEMP_TOKEN")
TEMP_USER = os.getenv("TEMP_USER")
TEMP_PASS = os.getenv("TEMP_PASS")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def verify_api_token(token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == TEMP_USER and form_data.password == TEMP_PASS:
        return {
            "access_token": API_TOKEN,
            "token_type": "bearer",
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/truck-noti")
def create_contact(request: TruckNoti, token: Annotated[str, Depends(verify_api_token)]):
    try:
        log_entry = f"""
                Garbage Truck Notification:
                Truck Number: {request.truck_no}
                Estimated Time of Arrival: {request.time}
                """
        log_to_file("../truck_logs.txt", log_entry.strip())

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL_ADDRESS
        msg["Subject"] = f"Grabage Truck Notification"

        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2c3e50;">📬 Garbage Truck Arriving</h2>
            <table cellspacing="0" cellpadding="8" border="0">
              <tr>
                <td><strong>Truck Number:</strong></td>
                <td>{request.truck_no}</td>
              </tr>
              <tr>
                <td><strong>Estimated Time of Arrival:</strong></td>
                <td>{request.time}</td>
              </tr>
            </table>
            <hr style="margin-top: 20px;" />
            <p style="font-size: 12px; color: #888;">This message was generated from your website contact form.</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL_ADDRESS, msg.as_string())

        return {"message": "Message sent"}
    except Exception as e:
        (print(e))


@router.post("/complaint")
async def signup(
    token: Annotated[str, Depends(verify_api_token)],
    issue_type: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    name: str = Form(...),
    mobile_number: int = Form(...),
    email: str = Form(...),
    evidence: UploadFile = File(...),
):
    try:
        log_entry = f"""
                Complaint:
                Issue: {issue_type}
                Location: {location}
                Description: {description}
                Name: {name}
                Email: {email}
                """
        log_to_file("../complaints_logs.txt", log_entry.strip())

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL_ADDRESS
        msg["Subject"] = "Complaint Registration"

        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2c3e50;">New Complaint Registration</h2>
            <table cellspacing="0" cellpadding="8" border="0">
              <tr><td><strong>Issue Type:</strong></td><td>{issue_type}</td></tr>
              <tr><td><strong>Location:</strong></td><td>{location}</td></tr>
              <tr><td><strong>Description:</strong></td><td>{description}</td></tr>
              <tr><td><strong>Name:</strong></td><td>{name}</td></tr>
              <tr><td><strong>Mobile Number:</strong></td><td>{mobile_number}</td></tr>
              <tr><td><strong>Email:</strong></td><td>{email}</td></tr>
            </table>
            <hr style="margin-top: 20px;" />
            <p style="font-size: 12px; color: #888;">This message was generated from your website signup form.</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        # Attach the evidence file
        file_bytes = await evidence.read()
        attachment = MIMEApplication(file_bytes, Name=evidence.filename)
        attachment["Content-Disposition"] = f'attachment; filename="{evidence.filename}"'
        msg.attach(attachment)

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL_ADDRESS, msg.as_string())

        return {"message": "Message sent"}
    except Exception as e:
        print(e)
        return {"error": str(e)}
