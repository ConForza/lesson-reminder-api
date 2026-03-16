from sqlalchemy.orm import Session

from app.db.models import LessonDB
from app.schemas.lesson import LessonResponse
from datetime import datetime


class LessonRepository:

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonResponse]:
        raise NotImplementedError

    def create_lesson(self, student_email, instrument, dt, duration):
        raise NotImplementedError


class InMemoryLessonRepository(LessonRepository):

    def __init__(self):
        self.lessons = [
            LessonResponse(
                id=1,
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 1, 6, 12, 30),
                duration=30,
            ),
            LessonResponse(
                id=2,
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 1, 15, 17, 0),
                duration=60,
            ),
            LessonResponse(
                id=3,
                student_email="joe@bloggs.com",
                instrument="piano",
                datetime=datetime(2026, 1, 28, 19, 30),
                duration=30,
            ),
            LessonResponse(
                id=4,
                student_email="john@smith.com",
                instrument="piano",
                datetime=datetime(2026, 2, 10, 14, 0),
                duration=0,
            ),
            LessonResponse(
                id=5,
                student_email="another@student.com",
                instrument="trumpet",
                datetime=datetime(2026, 2, 23, 18, 30),
                duration=30,
            )
        ]

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonResponse]:
        return [l for l in self.lessons if
                student_email == l.student_email and instrument == l.instrument]

    def create_lesson(self, student_email, instrument, dt, duration):
        id = self.lessons[-1].id + 1 if self.lessons is not None else 1
        lesson = LessonResponse(
                id=id,
                student_email=student_email,
                instrument=instrument,
                datetime=dt,
                duration=duration,
            )
        self.lessons.append(lesson)
        return lesson

class SqlAlchemyLessonRepository(LessonRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_lessons_for_student(self, student_email: str, instrument: str) -> list[LessonResponse]:
        lessons = []
        rows = (self.db.query(LessonDB)
                .filter(LessonDB.student_email == student_email, LessonDB.instrument == instrument))
        for row in rows:
            lessons.append(
                LessonResponse(
                    id=row.id,
                    student_email=row.student_email,
                    instrument=row.instrument,
                    datetime=row.datetime,
                    duration=row.duration,
                )
            )

        return lessons

    def create_lesson(self, student_email, instrument, dt, duration):
        db_lesson = LessonDB(
            student_email=student_email,
            instrument=instrument,
            datetime=dt,
            duration=duration,
        )
        self.db.add(db_lesson)
        self.db.commit()
        self.db.refresh(db_lesson)

        return LessonResponse(
            id=db_lesson.id,
            student_email=db_lesson.student_email,
            instrument=db_lesson.instrument,
            datetime=db_lesson.datetime,
            duration=db_lesson.duration,
        )
