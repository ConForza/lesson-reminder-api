from app.schemas.student import Student, StudentResponse


class StudentRepository:
    def get_student_by_email(self, email: str) -> Student | None:
        raise NotImplementedError

    def list_students(self):
        raise NotImplementedError

    def create_student(self, student: StudentResponse):
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