from typing import List

from fastapi import APIRouter, Depends, status
from routers.v1.dependencies import is_admin, localization
from schemas import models
from schemas.exception import ExceptionResponse
from schemas.success import SuccessResponse
from schemas.verify_status_set import VerifyStatusSet
from services import ManagerService, NoticeService, TenderService

router = APIRouter(
    prefix="/v1/manager",
    tags=["manager"],
)


@router.put(
    "/verification/{verification_id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
    tags=["verification"],
)
async def user_verification_response(
    verification_id: str,
    data: VerifyStatusSet,
    manager_service: ManagerService = Depends(),
    notice_service: NoticeService = Depends(),
) -> SuccessResponse:
    verf = await manager_service.get_verfication_request(
        verf_id=verification_id
    )
    user_id = verf.user_id
    await manager_service.response_user_verification_request(
        user_id=user_id,
        status=data.status,
        verf_id=verification_id,
        msg=data.message,
    )

    notice_type = "pass_verfication" if data.status else "not_pass_verfication"

    if data.status:
        await notice_service.add_notice(
            user_id=user_id,
            header=localization["notice"][notice_type]["header"],
            msg=localization["notice"][notice_type]["text"],
            href=None,
            href_text=None,
            href_color=None,
        )

    return SuccessResponse()


@router.get(
    "/users/",
    response_model=List[models.UserPrivateDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def get_users(
    manager_service: ManagerService = Depends(),
) -> List[models.UserPrivateDTO]:
    users = await manager_service.get_all_users()
    return users


@router.put(
    "/tender/{tender_id}/verify",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def update_tender_verified_status(
    tender_id: int,
    data: VerifyStatusSet,
    manager_service: ManagerService = Depends(),
    tender_service: TenderService = Depends(),
    notice_service: NoticeService = Depends(),
) -> SuccessResponse:
    await manager_service.update_tender_verified_status(
        tender_id=tender_id, status=data.status
    )

    tender = await tender_service.get_by_id(tender_id=tender_id)

    notice_type = (
        "tender_pass_verfication"
        if data.status
        else "tender_not_pass_verfication"
    )

    await notice_service.add_notice(
        user_id=tender.user_id,
        header=localization["notice"][notice_type]["header"],
        msg=localization["notice"][notice_type]["text"].format(
            tender.work_start.strftime("%d/%m/%Y в %H:%M")
        ),
        href=localization["notice"][notice_type]["href"]["link"].format(
            tender_id
        ),
        href_text=localization["notice"][notice_type]["href"]["text"],
        href_color=None,
    )

    return SuccessResponse()
