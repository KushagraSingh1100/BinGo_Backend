from routes.notification import verify_api_token
from fastapi import status, HTTPException, APIRouter
from schemas.schemas import Question as QuestionSchema, QuestionListResponse, QuestionSummary
from models.questions_model import Question
from fastapi import  Depends
from typing import Annotated


router = APIRouter(
    tags=['Questions'],
    prefix='/questions',
)

@router.post("/create")
async def create_question(request: QuestionSchema, token: Annotated[str, Depends(verify_api_token)]):
    """Create a new question"""
    question = await Question.create_new_question(
        course_id=request.course_id,
        question=request.question,
        option1=request.option1,
        option2=request.option2,
        option3=request.option3,
        option4=request.option4,
        correct_option=request.correct_option,
        marks=request.marks,
    )

    await question.save()

    return {
        "course_id": question.course_id,
        "question_id": question.question_id,
        "question": question.question,
        "option1": question.option1,
        "option2": question.option2,
        "option3": question.option3,
        "option4": question.option4,
        "correct_option": question.correct_option,
        "marks": question.marks,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }

@router.get("/course/{course_id}", response_model = QuestionListResponse)
async def get_questions_by_course(course_id: str):
    """ Get all the questions from a specific course"""

    questions = await Question.get_questions_by_course(course_id)

    questions_summaries = [
        QuestionSummary(
            course_id = question.course_id,
            question_id= question.question_id,
            question = question.question,
            option1 = question.option1,
            option2 = question.option2,
            option3 = question.option3,
            option4 = question.option4,
            correct_option=question.correct_option,
            marks = question.marks,
            created_at=question.created_at,
            updated_at=question.updated_at,
        )
        for question in questions
    ]
    return QuestionListResponse(questions=questions_summaries)

@router.get("/all", response_model = QuestionListResponse)
async def get_courses_by_question():
    """ Get all the questions"""

    questions = await Question.get_all_questions()

    questions_summaries = [
        QuestionSummary(
            course_id=question.course_id,
            question_id=question.question_id,
            question=question.question,
            option1=question.option1,
            option2=question.option2,
            option3=question.option3,
            option4=question.option4,
            correct_option=question.correct_option,
            marks=question.marks,
            created_at=question.created_at,
            updated_at=question.updated_at,
        )
        for question in questions
    ]
    return QuestionListResponse(questions=questions_summaries)

@router.get("/id/{question_id}", response_model = QuestionSchema)
async def get_question_by_id(question_id: str):
    """ Get a specific question by ID"""
    question = await Question.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question