from app.schemas.lesson import LessonSummary


class LessonRepository:

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonSummary]:
        return [l for l in InMemoryLessonRepository.lessons if
                student_email == l.student_email and instrument == l.instrument]


class InMemoryLessonRepository(LessonRepository):
    lessons = [
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
