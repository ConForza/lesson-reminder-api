from app.core.exceptions import DomainError
from app.schemas.remaining_lessons import RemainingLessonsResponse, RemainingLessonsRequest, Lesson
from app.schemas.student import StudentRequest, StudentResponse


class StudentService:

    def get_remaining_lessons(self, body: RemainingLessonsRequest) -> RemainingLessonsResponse:
        if body.student_email.strip() == "":
            raise DomainError("student_email must not be left blank")
        if body.instrument.lower().strip() != "piano":
            raise DomainError("Instrument is not supported")

        lessons = [
            Lesson(
                student_email="joe@bloggs.com",
                duration=30,
            ),
            Lesson(
                student_email="joe@bloggs.com",
                duration=60,
            ),
            Lesson(
                student_email="joe@bloggs.com",
                duration=30,
            ),
        ]
        lessons_30 = [l for l in lessons if l.duration == 30]
        lessons_60 = [l for l in lessons if l.duration == 60]

        return RemainingLessonsResponse(
            student_email=body.student_email,
            instrument=body.instrument,
            lessons_30=len(lessons_30),
            lessons_60=len(lessons_60),
        )

    def get_student(self, body: StudentRequest) -> StudentResponse:
        if body.student_email.strip() == "":
            raise DomainError("student_email must not be left blank")

        if body.student_email == "joe@bloggs.com":
            return StudentResponse(
                student_email=body.student_email,
                first_name="Joe",
                surname="Bloggs",
                instrument="piano",
            )
        else:
            raise DomainError("Student not found", status_code=404)