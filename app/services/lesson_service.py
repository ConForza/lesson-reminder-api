from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson import LessonCreateRequest, LessonResponse
from datetime import datetime
from app.core.exceptions import DomainError


class LessonService:

    def __init__(self, lesson_repo: LessonRepository):
        self.lesson_repo = lesson_repo

    def schedule_lesson(self, body: LessonCreateRequest) -> LessonResponse:
        lessons = self.lesson_repo.get_lessons_for_student(body.student_email, body.instrument)
        dt = datetime.strptime(body.date, "%d-%m-%y %H:%M")

        for lesson in lessons:
            if lesson.datetime == dt:
                raise DomainError("Lesson conflict: student already has a lesson at this time")

        lesson = self.lesson_repo.create_lesson(
            body.student_email,
            body.instrument,
            dt,
            body.duration
        )

        return lesson

