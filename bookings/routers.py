from fastapi import APIRouter, HTTPException, Request
from bookings.models import Booking, BookingStatus
from database import SessionDep
from bookings.schemas import BookingOutSchema, BookingCreateSchema
from sqlalchemy import select
from rate_limiter import rate_limit
from tasks.service import enqueue_booking

router = APIRouter(prefix="/api/bookings", tags=["Бронирования"])


@router.get(
    "/",
    response_model=list[BookingOutSchema],
    tags=["Бронь"],
    summary="Вывод списка бронирований"
)
async def get_bookings(
        session: SessionDep,
        status: BookingStatus | None = None,
        page: int = 1,
        size: int = 10
):
    page = max(page, 1)
    size = min(max(size, 1), 100)
    query = select(Booking)
    if status:
        query = query.where(Booking.status == status)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    result = await session.execute(query)
    bookings = result.scalars().all()
    return bookings


@router.get(
    "/{booking_id}",
    response_model=BookingOutSchema,
    tags=["Бронь"],
    summary="Вывод конкретной брони"
)
async def get_booking(
        session: SessionDep,
        booking_id: int
):
    booking = await session.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking



@router.post(
    "/",
    response_model=BookingOutSchema,
    tags=["Бронь"],
    summary="Создаёт очередь на создание брони"
)
async def create_booking(
        request: Request,
        booking: BookingCreateSchema,
        session: SessionDep
):
    ip = request.client.host

    if not rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests")
    db_booking = Booking(
        name=booking.name,
        datetime=booking.datetime,
        service_type=booking.service_type
    )
    session.add(db_booking)
    await session.commit()
    await session.refresh(db_booking)
    enqueue_booking(db_booking.id)
    return db_booking



@router.delete(
    "/{booking_id}",
    tags=["Бронь"],
    summary="Отмена брони"
)
async def delete_booking(
        booking_id: int,
        session: SessionDep
):
    booking = await session.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )
    if booking.status != BookingStatus.pending:
        raise HTTPException(
            status_code=400,
            detail="Only pending bookings can be deleted"
        )
    booking.status = BookingStatus.cancelled
    await session.commit()
    return "Deleted booking"
