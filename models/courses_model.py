from beanie import Document
from datetime import datetime
import uuid
from pymongo import ASCENDING, DESCENDING

class Course(Document):
    """
    Course Model
    """

    course_id: str
    title: str
    thumbnail: str
    description: str
    reward: int
    course_time: float
    questions: int
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "courses"

    @classmethod
    async def create_new_course(cls, course_title: str, course_thumbnail: str, description: str, reward: int, course_time: float, questions: int):
        """
        Create a new course
        """

        course_id = str(uuid.uuid4())

        course = cls(
            course_id=course_id,
            title=course_title,
            thumbnail=course_thumbnail,
            description=description,
            reward=reward,
            course_time=course_time,
            questions=questions,
            created_at=datetime.now(),
            updated_at=datetime.now(),

        )

        await course.insert()
        return course

    @classmethod
    async def get_courses_by_reward(cls, limit: int = 50):
        """Get all courses, ordered by most reward"""
        return await cls.find().sort(("reward", DESCENDING)).limit(limit).to_list()

    @classmethod
    async def get_courses_by_question(cls, limit: int = 50):
        """Get all courses, ordered by least questions"""
        return await cls.find().sort(("questions", ASCENDING)).limit(limit).to_list()

    @classmethod
    async def get_course_by_id(cls, course_id: str):
        """Get a specific course by ID"""
        return await cls.find_one({
            "course_id": course_id
        })
