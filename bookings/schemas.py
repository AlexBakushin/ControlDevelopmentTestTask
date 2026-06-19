from datetime import datetime
from pydantic import BaseModel
from bookings.models import BookingStatus


class BookingCreateSchema(BaseModel):
    name: str
    datetime: datetime
    service_type: str



class BookingOutSchema(BaseModel):
    id: int
    name: str
    datetime: datetime
    service_type: str
    status: BookingStatus

    model_config = {
        "from_attributes": True
    }