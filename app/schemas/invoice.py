from pydantic import BaseModel, Field
from typing import List

class InvoicePreviewRequest(BaseModel):
    staff_id: int = Field(examples=[1])
    date_from: str = Field(examples=["01-02-26"])
    date_to: str = Field(examples=["02-03-26"])
    preview: bool = Field(default=True, examples=[True])

class LessonPreview(BaseModel):
    name: str
    duration: int
    lesson_cut: float
    paid:bool

class InvoicePreviewResponse(BaseModel):
    staff_id: int
    date_from: str
    date_to: str
    preview: bool
    total_amount: float
    lessons: List[LessonPreview]