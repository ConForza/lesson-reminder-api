from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.health import health_router
from app.api.v1.invoice import invoice_router
from app.api.v1.students import students_router
from app.core.exceptions import DomainError

tags_metadata = [
    {"name": "system",
     "description": "System-level endpoints such as health checks."},
    {"name": "students",
     "description": "Endpoints related to student lesson tracking and calculations."},
    {"name": "invoices",
     "description": "Endpoints for invoice preview and generation logic."}
]

app = FastAPI(
    title="Lesson Reminder API",
    description="Backend API for managing student lessons and invoice tracking for a music school",
    version="0.1.0",
    openapi_tags=tags_metadata,
)
app.include_router(health_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(students_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
