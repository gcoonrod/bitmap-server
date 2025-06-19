
class CalendarDisplay:
    """
    A class to create a monochrome calendar display for a 2.9" ePaper display. 
    The display will show the current month, day, and weekday on the left half, 
    and the current time on the right half.
    """
    def __init__(self, out_dir: str = "./static"):
        self.width = 296
        self.height = 128
        self.color_depth = 1
        self.out_dir = out_dir

    def draw_calendar(self) -> str:
        from PIL import Image, ImageDraw, ImageFont

        # Create a new monochrome image
        image = Image.new("1", (self.width, self.height), 1)
        draw = ImageDraw.Draw(image)

        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except IOError:
            font = ImageFont.load_default()

        # Draw the left half with the current month, day, and weekday
        from datetime import datetime
        now = datetime.now()
        month = now.strftime("%B")
        day = now.day
        weekday = now.strftime("%A")
        left_text = f"{month} {day}\n{weekday}"
        draw.text((10, 10), left_text, font=font, fill=0)

        # Draw the right half with the current time
        time_text = now.strftime("%H:%M:%S")
        draw.text((self.width // 2 + 10, 10), time_text, font=font, fill=0)

        # Save the image to a file
        image.save(f"{self.out_dir}/calendar.bmp", "BMP")

        return f"{self.out_dir}/calendar.bmp"
