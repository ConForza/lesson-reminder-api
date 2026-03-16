from pydantic import BaseModel, ConfigDict


class Lesson(BaseModel):
    student_email: str
    duration: int

class RemainingLessonsRequest(BaseModel):
    student_email: str
    instrument: str

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "student_email": "student@example.com",
                "instrument": "piano",
            }
        }
    )

class RemainingLessonsResponse(BaseModel):
    student_email: str
    instrument: str
    lessons_30: int
    lessons_60: int
