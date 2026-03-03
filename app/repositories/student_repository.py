from sqlalchemy.orm import Session

from app.db.models import StudentDB
from app.schemas.student import Student, StudentResponse


class StudentRepository:
    def get_student_by_email(self, email: str) -> Student | None:
        raise NotImplementedError

    def list_students(self):
        raise NotImplementedError

    def create_student(self, student: StudentResponse):
        raise NotImplementedError

    def delete_student(self, email: str) -> None:
        raise NotImplementedError

    def update_student(self, email: str, student: StudentResponse):
        raise NotImplementedError

class InMemoryStudentRepository(StudentRepository):

    def __init__(self):
        self.students = [
            Student(
                student_email="joe@bloggs.com",
                first_name="Joe",
                surname="Bloggs",
                instrument="piano",
            )
        ]

    def get_student_by_email(self, email: str) -> Student | None:
        for student in self.students:
            if student.student_email == email:
                return student
        return None

    def list_students(self):
        return [s for s in self.students]

    def create_student(self, student: StudentResponse):
        self.students.append(
            Student(
                student_email=student.student_email,
                first_name=student.first_name,
                surname=student.surname,
                instrument=student.instrument,
            )
        )

    def delete_student(self, email: str) -> None:
        for i, student in enumerate(self.students):
            if student.student_email == email:
                del self.students[i]
                return
        raise ValueError("Student not found")

    def update_student(self, email: str, student: StudentResponse) -> None:
        for i, existing in enumerate(self.students):
            if existing.student_email == email:
                self.students[i] = Student(
                    student_email=email,
                    first_name=student.first_name,
                    surname=student.surname,
                    instrument=student.instrument,
                )
                return
        raise ValueError("Student not found")

class SqlAlchemyStudentRepository(StudentRepository):

    def __init__(self, db: Session):
        self.db = db
        self._ensure_seed_data()

    def _ensure_seed_data(self) -> None:
        existing = (
            self.db.query(StudentDB)
            .filter(StudentDB.student_email == "joe@bloggs.com")
            .first()
        )
        if existing is None:
            joe = StudentDB(
                student_email="joe@bloggs.com",
                first_name="Joe",
                surname="Bloggs",
                instrument="piano",
            )
            self.db.add(joe)
            self.db.commit()

    def get_student_by_email(self, email: str) -> Student | None:
        row = (
            self.db.query(StudentDB)
            .filter(StudentDB.student_email == email)
            .first()
        )
        if row is None:
            return None

        return Student(
            student_email=row.student_email,
            first_name=row.first_name,
            surname=row.surname,
            instrument=row.instrument,
        )

    def list_students(self) -> list[Student]:
        rows = self.db.query(StudentDB).all()
        return [
            Student(
            student_email=row.student_email,
            first_name=row.first_name,
            surname=row.surname,
            instrument=row.instrument,
        ) for row in rows
            ]

    def create_student(self, student: StudentResponse) -> None:
        db_student = StudentDB(
            student_email=student.student_email,
            first_name=student.first_name,
            surname=student.surname,
            instrument=student.instrument,
        )
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)

    def delete_student(self, email: str):
        row = (
            self.db.query(StudentDB)
            .filter(StudentDB.student_email == email)
            .first()
        )
        if row is None:
            raise ValueError("Student not found")

        self.db.delete(row)
        self.db.commit()

    def update_student(self, email: str, student: StudentResponse) -> None:
        row = (
            self.db.query(StudentDB)
            .filter(StudentDB.student_email == email)
            .first()
        )
        if row is None:
            raise ValueError("Student not found")

        row.first_name = student.first_name
        row.surname = student.surname
        row.instrument = student.instrument

        self.db.commit()
        self.db.refresh(row)
