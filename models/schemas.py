from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class TruckNoti(BaseModel):
    truck_no: str
    time: str

class Complaint(BaseModel):
    issue_type: str
    location: str
    description: str
    evidence: UploadFile
    name: str
    mobile_number: int
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    user_name: str
    password: str

