from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.health import health_router
from app.api.v1.invoice import invoice_router
from app.api.v1.students import students_router
from app.core.exceptions import DomainError

app = FastAPI()
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