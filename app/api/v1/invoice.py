from fastapi import APIRouter, Depends
from app.services.invoice_preview_service import InvoicePreviewService
from app.schemas.invoice import InvoicePreviewRequest, InvoicePreviewResponse

invoice_router = APIRouter(tags=["invoices"])

def get_invoice_preview_service() -> InvoicePreviewService:
    return InvoicePreviewService()

@invoice_router.post("/invoices/preview", response_model=InvoicePreviewResponse)
async def preview_invoice(
        body: InvoicePreviewRequest,
        service: InvoicePreviewService = Depends(get_invoice_preview_service)
):
    return service.preview_invoice(body)