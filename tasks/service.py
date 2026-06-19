from tasks.booking_tasks import process_booking


def enqueue_booking(booking_id: int):
    return process_booking.delay(booking_id)
