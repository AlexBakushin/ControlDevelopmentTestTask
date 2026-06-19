from fastapi import FastAPI, HTTPException
from bookings.routers import router as bookings_router
from database import new_session
from sqlalchemy import text
from logging_config import setup_logging
import logging

setup_logging()
app = FastAPI()
app.include_router(bookings_router)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health():
    try:
        # Проверка БД
        async with new_session() as session:
            await session.execute(text("SELECT 1"))

        return {"status": "ok"}

    except Exception as e:
        logger.info(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service Unavailable")
