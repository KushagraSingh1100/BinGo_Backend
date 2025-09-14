from beanie import init_beanie
import motor.motor_asyncio
from models.courses_model import Course
from models.questions_model import Question

async def init_db(mongo_uri: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongo_uri,
    )
    db = client["course_db"]
    await init_beanie(database=db, document_models=[Course, Question])

