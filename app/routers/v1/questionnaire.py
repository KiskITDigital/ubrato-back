from typing import List

from fastapi import APIRouter, Depends, Response, status
from routers.v1.dependencies import authorized, get_user, is_admin
from schemas.exception import ExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.models.questionnaire_answer import QuestionnaireAnswer
from schemas.questionnaire import QuestionnaireRequest
from schemas.success import SuccessResponse
from services.questionnaire import QuestionnaireService

router = APIRouter(
    prefix="/v1/questionnaire",
    tags=["questionnaire"],
)


@router.post(
    "/save",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def save(
    data: QuestionnaireRequest,
    questionnaire_service: QuestionnaireService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await questionnaire_service.save(data.answers, user.id)
    return SuccessResponse()


@router.get(
    "/answers",
    response_model=List[QuestionnaireAnswer],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def get_page(
    page: int = 1,
    page_size: int = 10,
    questionnaire_service: QuestionnaireService = Depends(),
) -> List[QuestionnaireAnswer]:
    return await questionnaire_service.get_page(page=page, page_size=page_size)


@router.get(
    "/answers/export",
    response_model=str,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def export(
    questionnaire_service: QuestionnaireService = Depends(),
) -> Response:
    response = Response(await questionnaire_service.export_csv())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
