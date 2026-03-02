from app.schemas.lesson import LessonSummary

class LessonRepository:

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonSummary]:
        raise NotImplementedError


class InMemoryLessonRepository(LessonRepository):

    def __init__(self):
        self.lessons = [
            LessonSummary(
                student_email="joe@bloggs.com",
                instrument="piano",
                duration=30,
            ),
            LessonSummary(
                student_email="joe@bloggs.com",
                instrument="piano",
                duration=60,
            ),
            LessonSummary(
                student_email="joe@bloggs.com",
                instrument="piano",
                duration=30,
            ),
            LessonSummary(
                student_email="john@smith.com",
                instrument="piano",
                duration=0,
            ),
            LessonSummary(
                student_email="another@student.com",
                instrument="trumpet",
                duration=30,
            )
        ]

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonSummary]:
        return [l for l in self.lessons if
                student_email == l.student_email and instrument == l.instrument]
