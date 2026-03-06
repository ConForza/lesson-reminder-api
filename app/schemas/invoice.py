from pydantic import BaseModel, Field
from typing import List
from datetime import date

class InvoicePreviewRequest(BaseModel):
    staff_id: int = Field(gt=0, examples=[1])
    date_from: date = Field(examples=["2026-02-28"])
    date_to: date = Field(examples=["2026-03-29"])
    preview: bool = Field(default=True, examples=[True])

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "staff_id": 1,
                "date_from": "2026-02-28",
                "date_to": "2026-03-29",
                "preview": True,
            }
        }

class LessonPreview(BaseModel):
    name: str
    duration: int
    lesson_cut: float
    paid:bool

class InvoicePreviewResponse(BaseModel):
    staff_id: int
    date_from: date
    date_to: date
    preview: bool
    total_amount: float
    lessons: List[LessonPreview]