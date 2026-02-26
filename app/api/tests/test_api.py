from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_invoice_preview():
    response = client.post("/api/v1/invoices/preview", json=(
        {
        "staff_id": 1,
        "date_from": "26-02-25",
        "date_to": "26-02-26",
        "preview": True,
         }
        )
    )

    data = response.json()

    assert response.status_code == 200
    assert data["total_amount"] == 25.0
    assert data["preview"] is True
    assert isinstance(data["lessons"], list)
    assert len(data["lessons"]) > 1

def test_students_remaining_lessons_blank_email():
    response = client.post("/api/v1/students/remaining-lessons", json=
    {
        "student_email": "",
        "instrument": "piano",
    }
)

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "student_email must not be left blank"}

def test_students_remaining_lessons_invalid_instrument():
    response = client.post("/api/v1/students/remaining-lessons", json=
    {
        "student_email": "joe@bloggs.com",
        "instrument": "trumpet",
    }
)

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "Instrument is not supported"}

def test_students_remaining_lessons():
    response = client.post("/api/v1/students/remaining-lessons", json=
    {
        "student_email": "joe@bloggs.com",
        "instrument": "piano",
    }
)

    data = response.json()

    assert response.status_code == 200
    assert data["lessons_30"] == 2
    assert data["lessons_60"] == 1