from typing import List
from app.schemas.invoice import LessonPreview, InvoicePreviewRequest, InvoicePreviewResponse

class InvoicePreviewService:

    def preview_invoice(self, body: InvoicePreviewRequest) -> InvoicePreviewResponse:
        lessons: List[LessonPreview] = [
            LessonPreview(
                name="Test Student 1",
                duration=30,
                lesson_cut=10.0,
                paid=True,
            ),

            LessonPreview(
                name = "Test Student 2",
                duration = 60,
                lesson_cut = 15.0,
                paid = False,
            ),
        ]

        total = sum(l.lesson_cut for l in lessons)

        return InvoicePreviewResponse(
            staff_id=body.staff_id,
            date_from=body.date_from,
            date_to=body.date_to,
            preview=body.preview,
            total_amount=total,
            lessons=lessons,
        )