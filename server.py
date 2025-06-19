from typing import Union, List, Tuple, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from datetime import datetime
from pytz import timezone as pytz_timezone, UnknownTimeZoneError

from bitmap_builder import BitmapBuilder
from fastapi.responses import Response

app = FastAPI()

class TimeResponse(BaseModel):
    current_time: str

@app.get("/health")
async def health_check() -> Union[dict[str, str], str]:
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

@app.get("/bitmap.bmp", response_class=FileResponse)
async def get_bitmap(width: int = 100, height: int = 100, color_depth: int = 1):
    """
    Endpoint to generate a bitmap image with specified dimensions and color depth.
    Returns the bitmap image as a byte array.
    
    :param width: Width of the bitmap image (default is 100).
    :param height: Height of the bitmap image (default is 100).
    :param color_depth: Color depth of the bitmap image (default is 1 for monochrome).
    """
    file = f"bitmap_{width}x{height}.bmp"
    path = f"./static/{file}"
    try:
        builder = BitmapBuilder(width, height, color_depth)
        builder.draw_rectangle(10, 10, width - 20, height - 20)  # Draw a red rectangle
        builder.save_image(f"./static/bitmap_{width}x{height}.bmp")  # Save to static directory
        return path
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/calendar.bmp", response_class=FileResponse)
async def get_calendar_bitmap():
    """
    Endpoint to generate a calendar bitmap image for the current month, day, weekday, and time.
    Returns the calendar image as a byte array.
    """
    from calendar_display import CalendarDisplay

    try:
        calendar_display = CalendarDisplay(out_dir="./static")
        file_path = calendar_display.draw_calendar()
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Mount static files directory for serving static content
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/files", response_class=FileResponse)
async def render_static_html(request: Request):
    #get directory listing of ./static
    import os
    static_files = os.listdir("./static")
    files: List[Dict[str, str]] = []

    for file in static_files:
        file_info: Dict[str, str] = {
            "name": str(file),
            "size": str(os.path.getsize(os.path.join("./static", file))),
            "created_at": datetime.fromtimestamp(os.path.getctime(os.path.join("./static", file))).strftime("%Y-%m-%d %H:%M:%S"),
        }
        files.append(file_info)

    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(request=request, name="static.html", context={"files": files})