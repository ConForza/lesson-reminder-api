from pydantic import BaseModel

class StudentRequest(BaseModel):
    student_email: str

class StudentResponse(BaseModel):
    student_email: str
    first_name: str
    surname: str
    instrument: str | None