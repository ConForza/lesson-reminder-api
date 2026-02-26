from pydantic import BaseModel

class Lesson(BaseModel):
    student_email: str
    duration: int

class RemainingLessonsRequest(BaseModel):
    student_email: str
    instrument: str

class RemainingLessonsResponse(BaseModel):
    student_email: str
    instrument: str
    lessons_30: int
    lessons_60: int
