from fastapi import UploadFile
from pydantic import BaseModel
from typing import List
from datetime import datetime

class TruckNoti(BaseModel):
    truck_no: str
    time: str

class Course(BaseModel):
    title: str
    thumbnail: str
    description: str
    reward: int
    course_time: float
    questions: int

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

class CourseSummary(BaseModel):
    course_id: str
    title: str
    thumbnail: str
    description: str
    reward: int
    course_time: float
    questions: int
    created_at: datetime
    updated_at: datetime

class CourseListResponse(BaseModel):
    courses: List[CourseSummary]

class Question(BaseModel):
    course_id: str
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_option: str
    marks: int

class QuestionSummary(BaseModel):
    course_id: str
    question_id: str
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_option: str
    marks: int
    created_at: datetime
    updated_at: datetime

class QuestionListResponse(BaseModel):
    questions: List[QuestionSummary]
