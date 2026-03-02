import pytest
from app.core.exceptions import DomainError
from app.repositories.lesson_repository import InMemoryLessonRepository
from app.repositories.student_repository import InMemoryStudentRepository
from app.services.student_service import StudentService
from app.schemas.remaining_lessons import RemainingLessonsRequest

class TestStudentService:

    student_service = StudentService(InMemoryLessonRepository(), InMemoryStudentRepository())

    def test_remaining_lessons_happy_path(self):
        request = RemainingLessonsRequest(
            student_email="joe@bloggs.com",
            instrument="piano",
        )

        response = self.student_service.get_remaining_lessons(request)

        assert response.student_email == "joe@bloggs.com"
        assert response.instrument == "piano"
        assert response.lessons_30 == 2
        assert response.lessons_60 == 1

    def test_blank_email(self):
        request = RemainingLessonsRequest(
            student_email="",
            instrument="piano",
        )

        with pytest.raises(DomainError, match="student_email must not be left blank"):
            self.student_service.get_remaining_lessons(request)


    def test_incorrect_instrument(self):
        request = RemainingLessonsRequest(
            student_email="joe@bloggs.com",
            instrument="trumpet",
        )

        with pytest.raises(DomainError, match="Instrument is not supported"):
            self.student_service.get_remaining_lessons(request)
