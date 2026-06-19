from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    failed = "failed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    datetime: Mapped[datetime] = mapped_column(DateTime)
    service_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[BookingStatus] = mapped_column(
        SQLEnum(
            BookingStatus,
            name="booking_status"
        ),
        default=BookingStatus.pending
    )