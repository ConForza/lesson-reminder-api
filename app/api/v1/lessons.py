from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.core.deps import get_lesson_service
from app.services.lesson_service import LessonService
from app.schemas.lesson import LessonResponse, LessonCreateRequest

lessons_router = APIRouter(tags=["lessons"], dependencies=[Depends(get_current_user)])

@lessons_router.post("/lessons", response_model=LessonResponse, status_code=201)
async def create_lesson(
    body: LessonCreateRequest,
    service: LessonService = Depends(get_lesson_service),
) -> LessonResponse:
    return service.schedule_lesson(body)