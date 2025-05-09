import time
import itertools
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13v4  # Use the epd2in13v4 module

def draw_tree(draw, offset, width, height):
    """
    Draw a simple tree with a fixed trunk and swaying foliage.
    
    Args:
        draw: PIL ImageDraw object to draw on the image.
        offset: X-coordinate of the foliage center (varies to simulate swaying).
        width: Display width in pixels.
        height: Display height in pixels.
    """
    # Draw trunk (fixed position)
    trunk_left = width // 2 - 10
    trunk_top = height - 50
    trunk_right = width // 2 + 10
    trunk_bottom = height
    draw.rectangle([(trunk_left, trunk_top), (trunk_right, trunk_bottom)], fill=0)  # Black

    # Draw foliage (sways left and right)
    foliage_center = (offset, height - 70)
    radius = 30
    draw.ellipse([(foliage_center[0] - radius, foliage_center[1] - radius),
                  (foliage_center[0] + radius, foliage_center[1] + radius)], fill=0)  # Black

try:
    # Initialize the e-Paper display
    epd = epd2in13v4.EPD()
    epd.init(epd.PARTIAL)  # Initialize for partial refresh
    epd.Clear(255)  # Clear display to white (255 = white for 1-bit images)

    # Get display dimensions
    width = epd.width
    height = epd.height

    # Define foliage offsets for swaying animation (left, center, right, center)
    offsets = [width // 2 - 10, width // 2, width // 2 + 10, width // 2]
    offset_cycle = itertools.cycle(offsets)  # Cycle through offsets indefinitely

    # Animation loop
    while True:
        # Create a new 1-bit image (black and white)
        image = Image.new('1', (width, height), 255)  # 255 = white background
        draw = ImageDraw.Draw(image)

        # Get the next offset and draw the tree
        offset = next(offset_cycle)
        draw_tree(draw, offset, width, height)

        # Display the image on the e-Paper using partial refresh
        epd.displayPartial(image)

        # Wait 1 second before the next frame
        time.sleep(1)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    epd.sleep()
    print("Display sleeping")
except Exception as e:
    # Print any errors that occur
    print(f"Error: {e}")