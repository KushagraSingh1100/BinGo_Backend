from routes.notification import verify_api_token
from fastapi import status, HTTPException, APIRouter
from schemas.schemas import Course as CourseSchema, CourseListResponse, CourseSummary
from models.courses_model import Course
from fastapi import  Depends
from typing import Annotated


router = APIRouter(
    tags=['Course'],
    prefix='/courses',
)

@router.post("/create")
async def create_course(request: CourseSchema, token: Annotated[str, Depends(verify_api_token)]):
    """Create a new course"""
    course = await Course.create_new_course(
        course_title=request.title,
        course_thumbnail=request.thumbnail,
        description=request.description,
        reward=request.reward,
        course_time=request.course_time,
        questions=request.questions,
    )

    await course.save()

    return {
        "course_id": course.course_id,
        "title": course.title,
        "created_at": course.created_at
    }

@router.get("/reward", response_model = CourseListResponse)
async def get_courses_by_reward():
    """ Get all the courses sorted by reward """

    courses = await Course.get_courses_by_reward()

    courses_summaries = [
        CourseSummary(
            course_id = course.course_id,
            title = course.title,
            thumbnail = course.thumbnail,
            description = course.description,
            reward = course.reward,
            course_time = course.course_time,
            questions = course.questions,
            created_at = course.created_at,
            updated_at= course.updated_at,
        )
        for course in courses
    ]
    return CourseListResponse(courses=courses_summaries)
@router.get("/questions", response_model = CourseListResponse)
async def get_courses_by_question():
    """ Get all the courses sorted by question """

    courses = await Course.get_courses_by_question()

    courses_summaries = [
        CourseSummary(
            course_id = course.course_id,
            title = course.title,
            thumbnail = course.thumbnail,
            description = course.description,
            reward = course.reward,
            course_time = course.course_time,
            questions = course.questions,
            created_at = course.created_at,
            updated_at= course.updated_at,
        )
        for course in courses
    ]
    return CourseListResponse(courses=courses_summaries)