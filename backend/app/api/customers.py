from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.schemas import CustomerDetailRead, CustomerRead, DeviceRead, ServiceRead
from app.services import ticket_queries
from app.services.ticket_queries import CustomerNotFoundError

router = APIRouter(prefix="/customers", tags=["customers"])


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
        services=[ServiceRead.model_validate(service) for service in record.services],
        devices=[
            DeviceRead(
                id=device.id,
                device_ref=device.device_ref,
                device_type=device.device_type,
                name=device.name,
                status=device.status,
                credential_available=device.credential_available,
            )
            for device in record.devices
        ],
    )
