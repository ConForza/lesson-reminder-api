# Lesson Reminder API

A FastAPI backend for managing student lesson tracking and invoice preview logic for a music school.

This project demonstrates layered architecture, domain-driven validation, dependency injection, and API-level testing using FastAPI and Pytest.

---

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Project Structure

- `app/api/v1/` – FastAPI routers
- `app/services/` – Business logic layer
- `app/schemas/` – Pydantic request/response models
- `app/core/` – Domain exceptions and core utilities
- `app/api/tests/` – API integration tests using FastAPI TestClient

---

## Running the Application

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Development Server

```bash
uvicorn app.main:app --reload
```

---

## Running Tests

Run all tests with:
```bash
python -m pytest
```
The test suite includes:
	•	Service-level tests for business logic
	•	API-level tests using FastAPI TestClient
	•	Validation and error-handling tests
	•	Domain exception handling tests

---

## API Endpoints

System
	•	GET /api/v1/health

⸻

Students
	•	POST /api/v1/students/remaining-lessons
	•	GET /api/v1/students/{student_email}
	•	GET /api/v1/students/{student_email}/remaining-lessons

⸻

Invoices
	•	POST /api/v1/invoices/preview

Dates for invoice preview are expected in DD-MM-YY format.

---

## Architecture

The application follows a layered architecture:
	•	Routers handle HTTP concerns.
	•	Services contain business logic.
	•	Schemas define request and response models.
	•	Domain errors are raised in the service layer and handled globally via a custom exception handler.

This separation ensures that business logic remains independent of the HTTP layer and allows external integrations (such as scheduling providers) to be swapped without affecting core domain logic.
