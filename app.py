from fastapi import FastAPI
from courses_database import database
from fastapi.middleware.cors import CORSMiddleware
from routes.notification import router as notifications_router
from routes.courses import router as courses_router
from routes.questions import router as questions_router
import os
from dotenv import load_dotenv

load_dotenv(".env.development")

# Now you can access environment variables
MONGO_URL = os.getenv("MONGO_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    await database.init_db(MONGO_URL)
app.include_router(notifications_router)
app.include_router(courses_router)
app.include_router(questions_router)