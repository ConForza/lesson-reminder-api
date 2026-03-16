from pydantic import BaseModel, EmailStr, ConfigDict


class StudentRequest(BaseModel):
    student_email: str

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "student_email": "student@example.com",
            }
        }
    )

class StudentResponse(BaseModel):
    student_email: EmailStr
    first_name: str
    surname: str
    instrument: str | None

class Student(BaseModel):
    student_email: str
    first_name: str
    surname: str
    instrument: str | None

class CreateStudentRequest(BaseModel):
    student_email: EmailStr
    first_name: str
    surname: str
    instrument: str

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "student_email": "student@example.com",
                "first_name": "Joe",
                "surname": "Bloggs",
                "instrument": "piano",
            }
        }
    )

class UpdateStudentRequest(BaseModel):
    first_name: str
    surname: str
    instrument: str

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "first_name": "Joe",
                "surname": "Bloggs",
                "instrument": "piano",
            }
        }
    )