from fastapi import APIRouter, Depends
from app.schemas.student import StudentRequest, StudentResponse
from app.services.student_service import StudentService
from app.schemas.remaining_lessons import RemainingLessonsResponse, RemainingLessonsRequest

students_router = APIRouter(tags=["students"])

def get_student_service() -> StudentService:
    return StudentService()


@students_router.get(
    "/students/{student_email}",
    response_model=StudentResponse,
    summary="Get a student's record",
    description="Returns the student's first name, surname and instrument for the given email. "
                "Student email must not be left blank."
)
async def get_student_record(
        student_email: str,
        service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    return service.get_student(
        StudentRequest(
            student_email=student_email,
        )
    )

@students_router.post(
    "/students/remaining-lessons",
    response_model=RemainingLessonsResponse,
    summary="Calculate remaining lessons for a student",
    description="Returns the number of remaining 30-minute and 60-minute lessons for a given student and instrument. "
                "Currently supports piano only. student_email must not be left blank."
)
async def remaining_lessons(
        body: RemainingLessonsRequest,
        service: StudentService = Depends(get_student_service)
) -> RemainingLessonsResponse:
    return service.get_remaining_lessons(body)


@students_router.get(
    "/students/{student_email}/remaining-lessons",
    response_model=RemainingLessonsResponse,
    summary = "Get remaining lessons for a student",
    description = "Returns the number of lessons for a student using path and query parameters. "
              "Currently supports piano only. student_email must not be left blank."
)
async def get_remaining_lessons(student_email: str, instrument: str,
                                service: StudentService = Depends(get_student_service)) -> RemainingLessonsResponse:
    return service.get_remaining_lessons(
        RemainingLessonsRequest(
            student_email=student_email,
            instrument=instrument,
        )
    )
