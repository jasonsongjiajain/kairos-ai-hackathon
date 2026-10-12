from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.schemas import (
    CustomerDetailRead,
    CustomerRead,
    CustomerSummaryRead,
    DeviceRead,
    NetworkCustomerRead,
    RouterRead,
    ServiceRead,
    find_credential,
)
from app.services import ticket_queries
from app.services.ticket_queries import CustomerNotFoundError

router = APIRouter(prefix="/customers", tags=["customers"])


def _device_read(device: ticket_queries.DeviceRecord) -> DeviceRead:
    read = DeviceRead.model_validate(device.source)
    read.credential_available = device.credential_available
    return read


@router.get("", response_model=list[NetworkCustomerRead])
def list_customers(
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[NetworkCustomerRead]:
    records = ticket_queries.list_network_customers(session, user)
    return [
        NetworkCustomerRead(
            customer=CustomerRead.model_validate(record.customer),
            devices=[DeviceRead.model_validate(device) for device in record.devices],
            routers=[RouterRead.model_validate(router) for router in record.routers],
            summary=CustomerSummaryRead.model_validate(record.summary) if record.summary else None,
        )
        for record in records
    ]


@router.get("/{customer_id}", response_model=CustomerDetailRead)
def get_customer(
    customer_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> CustomerDetailRead:
    try:
        record = ticket_queries.get_customer_detail(session, customer_id, user)
    except CustomerNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found") from error

    return CustomerDetailRead(
        customer=CustomerRead.model_validate(record.customer),
        services=[
            ServiceRead(
                id=service.id,
                service_type=service.service_type,
                service_ref=service.service_ref,
                status=service.status,
                details=service.details,
                credential_available=find_credential(service.details) is not None,
            )
            for service in record.services
        ],
        devices=[_device_read(device) for device in record.devices],
        routers=[RouterRead.model_validate(router) for router in record.routers],
        customer_summary=CustomerSummaryRead.model_validate(record.customer_summary) if record.customer_summary else None,
    )
