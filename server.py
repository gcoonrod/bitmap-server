from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from datetime import datetime
from pytz import timezone as pytz_timezone, UnknownTimeZoneError

app = FastAPI()

class TimeResponse(BaseModel):
    current_time: str

@app.get("/health")
async def health_check() -> Union[dict, str]:
    """
    Health check endpoint to verify if the server is running.
    Returns a simple message indicating the server is healthy.
    """
    return {"status": "healthy"}

@app.get("/time", response_model=TimeResponse)
async def get_current_time(timezone: str = "UTC") -> TimeResponse:
    """
    Endpoint to get the current server time.
    Returns the current time in a structured format.
    Accepts an optional timezone query parameter.
    """

    try:
        tz = pytz_timezone(timezone)
    except UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    return TimeResponse(current_time=current_time)