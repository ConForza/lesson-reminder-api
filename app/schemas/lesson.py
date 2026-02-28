from pydantic import BaseModel


class LessonSummary(BaseModel):
    student_email: str
    instrument: str
    duration: int