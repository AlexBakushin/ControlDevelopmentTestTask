import random
import asyncio
from tasks.celery_app import celery_app
from database import new_session
from bookings.models import Booking, BookingStatus
import logging

logger = logging.getLogger(__name__)


async def process_booking_async(booking_id: int):
    await asyncio.sleep(5)
    async with new_session() as session:
        booking = await session.get(Booking, booking_id)

        if booking is None:
            return

        if booking.status != BookingStatus.pending:
            return

        if random.random() < 0.15:
            booking.status = BookingStatus.failed
            await session.commit()
            raise Exception("External service failed")

        booking.status = BookingStatus.confirmed
        await session.commit()
        logger.info(f"Notification sent for booking", extra={"booking_id": booking_id})


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
)
def process_booking(self, booking_id: int):
    asyncio.run(process_booking_async(booking_id))