from anyio.functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.lesson_repository import LessonRepository, InMemoryLessonRepository
from app.repositories.student_repository import StudentRepository, SqlAlchemyStudentRepository
from app.services.invoice_preview_service import InvoicePreviewService
from app.services.student_service import StudentService

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_lesson_repository() -> LessonRepository:
    return InMemoryLessonRepository()

def get_student_repository(db: Session = Depends(get_db)) -> StudentRepository:
    return SqlAlchemyStudentRepository(db)

def get_student_service(lesson_repo: LessonRepository = Depends(get_lesson_repository),
                        student_repo: StudentRepository = Depends(get_student_repository)) -> StudentService:
    return StudentService(lesson_repo, student_repo)

@lru_cache
def get_invoice_preview_service() -> InvoicePreviewService:
    return InvoicePreviewService()