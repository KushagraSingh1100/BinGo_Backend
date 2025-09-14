from beanie import Document
from datetime import datetime
import uuid
from pymongo import ASCENDING, DESCENDING

class Question(Document):
    """
    Question Model
    """

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

    class Settings:
        name = "questions"

    @classmethod
    async def create_new_question(cls, course_id: str, question: str, option1: str, option2: str, option3: str, option4: str, correct_option: str, marks: int):
        """
        Create a new question
        """

        question_id = str(uuid.uuid4())

        question = cls(
            course_id=course_id,
            question_id=question_id,
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            marks=marks,
            created_at=datetime.now(),
            updated_at=datetime.now(),

        )

        await question.insert()
        return question

    @classmethod
    async def get_questions_by_course(cls, course_id: str, limit: int = 50):
        """Get all questions from a specific course"""
        return await cls.find(cls.course_id == course_id).sort(-cls.updated_at).limit(limit).to_list()

    @classmethod
    async def get_all_questions(cls, limit: int = 50):
        """Get all questions"""
        return await cls.find().limit(limit).to_list()

    @classmethod
    async def get_question_by_id(cls, question_id: str):
        """Get a specific question by ID"""
        return await cls.find_one({
            "question_id": question_id
        })
