from PIL import Image, ImageDraw


class BitmapBuilder:
    """BitmapBuilder is a class for building bitmap images with specified width, height, and color depth."""
    
    def __init__(self, width: int, height: int, color_depth: int = 1):
        """
        Initializes the BitmapBuilder with specified width, height, and color depth.

        :param width: Width of the bitmap image.
        :param height: Height of the bitmap image.
        :param color_depth: Color depth of the bitmap image (e.g., 24 for RGB). Default is 1 (monochrome).
        :raises ValueError: If width or height is less than or equal to zero, or if color depth is not a positive integer.
        """
        self.width = width
        self.height = height
        self.color_depth = color_depth
        self.bitmap_data = bytearray()

        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be greater than zero.")
        if color_depth <= 0:
            raise ValueError("Color depth must be a positive integer.")
        
        self.image = Image.new(mode="RGB" if color_depth == 24 else "1", size=(width, height))

    def get_bitmap(self):
        """
        Returns the bitmap image as a byte array suitable for serving over HTTP.
        :return: Byte array of the bitmap image.
        """
        return self.image.tobitmap()
        

    def draw_rectangle(self, x: int, y: int, width: int, height: int):
        """
        Draws a rectangle on the bitmap image.

        :param x: X coordinate of the top-left corner of the rectangle.
        :param y: Y coordinate of the top-left corner of the rectangle.
        :param width: Width of the rectangle.
        :param height: Height of the rectangle.
        :param color: Color of the rectangle in RGB format (tuple).
        """
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x, y, x + width, y + height])

    def save_image(self, filename: str):
        """
        Saves the bitmap image to a file.

        :param filename: The name of the file to save the bitmap image.
        """
        self.image.save(filename, format="BMP")