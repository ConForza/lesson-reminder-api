from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invoice_preview():
    response = client.post("/api/v1/invoices/preview", json=
    {
        "staff_id": 1,
        "date_from": "2025-02-26",
        "date_to": "2026-02-26",
        "preview": True,
    }
                           )

    data = response.json()

    assert response.status_code == 200
    assert data["total_amount"] == 25.0
    assert data["preview"] is True
    assert isinstance(data["lessons"], list)
    assert len(data["lessons"]) > 1


def test_invalid_staff_id_in_invoice_preview():
    response = client.post("/api/v1/invoices/preview", json=
    {
        "staff_id": 0,
        "date_from": "2025-02-26",
        "date_to": "2026-02-26",
        "preview": True,
    }

                           )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Input should be greater than 0"


def test_blank_date_from_in_invoice_preview():
    response = client.post("/api/v1/invoices/preview", json=
    {
        "staff_id": 1,
        "date_from": "",
        "date_to": "2026-02-26",
        "preview": True,
    }
                           )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Input should be a valid date or datetime, input is too short"


def test_blank_date_to_in_invoice_preview():
    response = client.post("/api/v1/invoices/preview", json=
    {
        "staff_id": 1,
        "date_from": "2026-02-26",
        "date_to": "",
        "preview": True,
    }
                           )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Input should be a valid date or datetime, input is too short"


def test_date_from_greater_than_date_to():
    response = client.post("/api/v1/invoices/preview", json=
    {
        "staff_id": 1,
        "date_from": "2026-02-26",
        "date_to": "2026-02-25",
        "preview": True,
    }
                           )

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "date_to must not be before date_from"}


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
    response = client.post(
        "/api/v1/students/remaining-lessons",
        json=
        {
            "student_email": "joe@bloggs.com",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["lessons_30"] == 2
    assert data["lessons_60"] == 1


def test_get_remaining_lessons():
    response = client.get("/api/v1/students/joe@bloggs.com/remaining-lessons?instrument=piano")

    data = response.json()

    assert response.status_code == 200
    assert data["lessons_30"] == 2
    assert data["lessons_60"] == 1
    assert data["student_email"] == "joe@bloggs.com"
    assert data["instrument"] == "piano"


def test_get_remaining_lessons_blank_email():
    response = client.get("/api/v1/students/%20/remaining-lessons?instrument=piano")

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "student_email must not be left blank"}


def test_get_remaining_lessons_invalid_instrument():
    response = client.get("/api/v1/students/joe@bloggs.com/remaining-lessons?instrument=trumpet")

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "Instrument is not supported"}


def test_get_student():
    response = client.get("/api/v1/students/joe@bloggs.com")

    data = response.json()

    assert response.status_code == 200
    assert data["first_name"] == "Joe"
    assert data["surname"] == "Bloggs"
    assert data["instrument"] == "piano"


def test_get_student_with_blank_email():
    response = client.get("/api/v1/students/%20")

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "student_email must not be left blank"}


def test_get_student_with_unknown_email():
    response = client.get("/api/v1/students/unknown@person.com")

    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "Student not found"}


def test_create_student():
    response = client.post(
        "/api/v1/students",
        json={
            "student_email": "another@student.com",
            "first_name": "Another",
            "surname": "Student",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["student_email"] == "another@student.com"
    assert data["first_name"] == "Another"
    assert data["surname"] == "Student"
    assert data["instrument"] == "piano"

def test_create_student_with_duplicate_email():
    response = client.post(
        "/api/v1/students",
        json={
            "student_email": "joe@bloggs.com",
            "first_name": "Joe",
            "surname": "Bloggs",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Student already exists"

def test_create_student_and_fetch_all_students():
    client.post(
        "/api/v1/students",
        json={
            "student_email": "another@student.com",
            "first_name": "Another",
            "surname": "Student",
            "instrument": "piano",
        }
    )

    response = client.get("/api/v1/students")

    data = response.json()

    assert response.status_code == 200
    assert data == [{
            "student_email": "joe@bloggs.com",
            "first_name": "Joe",
            "surname": "Bloggs",
            "instrument": "piano",
        },
        {
            "student_email": "another@student.com",
            "first_name": "Another",
            "surname": "Student",
            "instrument": "piano",
        }
    ]

def test_delete_student():
    client.post(
        "api/v1/students",
        json={
            "student_email": "delete@test.com",
            "first_name": "Delete",
            "surname": "Me",
            "instrument": "piano",
        }
    )

    response = client.delete("/api/v1/students/delete@test.com")
    data = response.json()

    assert response.status_code == 200
    assert data == {"detail": "Student deleted successfully"}

def test_delete_non_existent_student():
    response = client.delete("/api/v1/students/unknown@test.com")

    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "Student not found"}

def test_update_student():
    response = client.put(
        "/api/v1/students/joe@bloggs.com",
        json={
            "first_name": "Joseph",
            "surname": "Bloggs",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["student_email"] == "joe@bloggs.com"
    assert data["first_name"] == "Joseph"
    assert data["surname"] == "Bloggs"
    assert data["instrument"] == "piano"

def test_update_student_blank_email():
    response = client.put(
        "/api/v1/students/%20",
        json={
            "first_name": "Whatever",
            "surname": "Name",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "student_email must not be left blank"}

def test_update_non_existent_student():
    response = client.put(
        "/api/v1/students/doesnotexist@test.com",
        json={
            "first_name": "Ghost",
            "surname": "User",
            "instrument": "piano",
        }
    )

    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "Student not found"}