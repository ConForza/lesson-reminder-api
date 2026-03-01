from fastapi import Depends

from app.repositories.lesson_repository import LessonRepository, InMemoryLessonRepository
from app.services.invoice_preview_service import InvoicePreviewService
from app.services.student_service import StudentService

def get_lesson_repository() -> LessonRepository:
    return InMemoryLessonRepository()

def get_student_service(repo: LessonRepository = Depends(get_lesson_repository)) -> StudentService:
    return StudentService(repo)

def get_invoice_preview_service() -> InvoicePreviewService:
    return InvoicePreviewService()