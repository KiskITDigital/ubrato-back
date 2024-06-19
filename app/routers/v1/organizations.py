from fastapi import APIRouter, Depends, status
from repositories.postgres.schemas import (
    ContractorLocation,
    ContractorObject,
    ContractorService,
    CustomerLocation,
)
from routers.v1.dependencies import authorized, get_user, localization
from schemas import models
from schemas.exception import ExceptionResponse, UnauthExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.success import SuccessResponse
from schemas.update_profile import (
    ContractorCVRequest,
    ContractorCVResponse,
    UpdateBrandContactRequest,
    UpdateBrandProfileRequest,
    UpdateContractorProfileRequest,
    UpdateCustomerProfileRequest,
)
from services import OrganizationService
from services.exceptions import ServiceException

router = APIRouter(
    prefix="/v1/organizations",
    tags=["organizations"],
)


@router.get(
    "/profile/{org_id}/customer",
    response_model=models.CustomerProfile,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_customer_profile(
    org_id: str, org_service: OrganizationService = Depends()
) -> models.CustomerProfile:
    return await org_service.get_customer_profile(org_id)


@router.get(
    "/profile/{org_id}/contractor",
    response_model=models.ContractorProfile,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_contractor_profile(
    org_id: str, org_service: OrganizationService = Depends()
) -> models.ContractorProfile:
    return await org_service.get_contractor_profile(org_id)


@router.get(
    "/profile/{org_id}",
    response_model=models.OrganizationDTO,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_organization_profile(
    org_id: str, org_service: OrganizationService = Depends()
) -> models.Organization:
    return (await org_service.get_organization_by_id(org_id)).to_model()


@router.get(
    "/my/profile/customer",
    response_model=models.CustomerProfile,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_my_customer_profile(
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.CustomerProfile:
    return await org_service.get_customer_profile(user.org_id)


@router.get(
    "/my/profile/contractor",
    response_model=models.ContractorProfile,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_my_contractor_profile(
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.ContractorProfile:
    return await org_service.get_contractor_profile(user.org_id)


@router.put(
    "/my/profile/customer",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_my_customer_profile(
    data: UpdateCustomerProfileRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await org_service.update_customer_info(
        org_id=user.org_id, description=data.description
    )
    await org_service.set_customer_locations(
        org_id=user.org_id,
        locations=[
            CustomerLocation(org_id=user.org_id, city_id=city_id)
            for city_id in data.locations
        ],
    )
    return SuccessResponse()


@router.put(
    "/my/profile/contractor",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_my_contractor_profile(
    data: UpdateContractorProfileRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await org_service.update_contractor_info(
        org_id=user.org_id, description=data.description
    )
    await org_service.set_contractor_locations(
        org_id=user.org_id,
        locations=[
            ContractorLocation(org_id=user.org_id, city_id=city_id)
            for city_id in data.locations
        ],
    )
    await org_service.set_contractor_services(
        org_id=user.org_id,
        services=[
            ContractorService(
                org_id=user.org_id,
                service_type_id=service.id,
                price=service.price,
            )
            for service in data.services
        ],
    )
    await org_service.set_contractor_objects(
        org_id=user.org_id,
        objects=[
            ContractorObject(org_id=user.org_id, object_type_id=object_id)
            for object_id in data.objects
        ],
    )
    return SuccessResponse()


@router.post(
    "/my/profile/cv",
    response_model=ContractorCVResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def save_my_cv(
    data: ContractorCVRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> ContractorCVResponse:
    id = await org_service.save_contractor_cv(
        org_id=user.org_id,
        name=data.name,
        description=data.description,
        links=data.links,
    )
    return ContractorCVResponse(id=id)


@router.put(
    "/my/profile/cv/{cv_id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_my_cv(
    cv_id: str,
    data: ContractorCVRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    cv = await org_service.get_contractor_cv_by_id(cv_id=cv_id)
    if cv.org_id != user.org_id:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
    await org_service.update_contractor_cv(cv_id=cv_id, cv=data.__dict__)
    return SuccessResponse()


@router.delete(
    "/my/profile/cv/{cv_id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def delete_my_cv(
    cv_id: str,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    cv = await org_service.get_contractor_cv_by_id(cv_id=cv_id)
    if cv.org_id != user.org_id:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
    await org_service.delete_contractor_cv(cv_id=cv_id)
    return SuccessResponse()


@router.get(
    "/my",
    response_model=models.Organization,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_my_org(
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.Organization:
    return (
        await org_service.get_organization_by_id(org_id=user.org_id)
    ).to_model()


@router.put(
    "/my/profile/brand",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_my_brand_profile(
    data: UpdateBrandProfileRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await org_service.set_brand_name(user.org_id, data.name)
    await org_service.set_brand_avatar(user.org_id, data.avatar)

    return SuccessResponse()


@router.put(
    "/my/profile/brand/contacts",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_my_brand_contacts(
    data: UpdateBrandContactRequest,
    org_service: OrganizationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await org_service.set_brand_contact_info(
        org_id=user.org_id,
        emails=[(email.contact, email.info) for email in data.emails],
        phones=[(phone.contact, phone.info) for phone in data.phones],
        messengers=[
            (messenger.contact, messenger.info)
            for messenger in data.messengers
        ],
    )

    return SuccessResponse()
