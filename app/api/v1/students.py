from fastapi import APIRouter, Depends, HTTPException
from app.services.student_service import StudentService
from app.schemas.remaining_lessons import RemainingLessonsResponse, RemainingLessonsRequest

students_router = APIRouter(tags=["students"])

def get_student_service() -> StudentService:
    return StudentService()

@students_router.post("/students/remaining-lessons", response_model=RemainingLessonsResponse)
async def remaining_lessons(
        body: RemainingLessonsRequest,
        service: StudentService = Depends(get_student_service)
) -> RemainingLessonsResponse:
    try:
        return service.get_remaining_lessons(body)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))