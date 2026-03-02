from anyio.functools import lru_cache
from fastapi import Depends

from app.repositories.lesson_repository import LessonRepository, InMemoryLessonRepository
from app.repositories.student_repository import StudentRepository, InMemoryStudentRepository
from app.services.invoice_preview_service import InvoicePreviewService
from app.services.student_service import StudentService

def get_lesson_repository() -> LessonRepository:
    return InMemoryLessonRepository()

@lru_cache
def get_student_repository() -> StudentRepository:
    return InMemoryStudentRepository()

def get_student_service(lesson_repo: LessonRepository = Depends(get_lesson_repository),
                        student_repo: StudentRepository = Depends(get_student_repository)) -> StudentService:
    return StudentService(lesson_repo, student_repo)

def get_invoice_preview_service() -> InvoicePreviewService:
    return InvoicePreviewService()