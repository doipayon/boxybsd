from PIL import Image, ImageDraw
from math import sin, cos, radians
from datetime import datetime

def draw_clock():
    # Clock parameters
    width, height = 400, 400
    center = width // 2
    radius = center - 20

    # Create a blank canvas
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw the clock face
    draw.ellipse((20, 20, width - 20, height - 20), outline="black", width=4)

    # Draw clock numbers (12, 3, 6, 9)
    font_size = 20
    draw.text((center - 10, 30), "12", fill="black")
    draw.text((width - 40, center - 10), "3", fill="black")
    draw.text((center - 10, height - 40), "6", fill="black")
    draw.text((30, center - 10), "9", fill="black")

    # Get the current time
    now = datetime.now()
    hour, minute, second = now.hour % 12, now.minute, now.second

    # Convert time to angles
    second_angle = radians((second / 60) * 360 - 90)
    minute_angle = radians((minute / 60) * 360 - 90)
    hour_angle = radians(((hour + minute / 60) / 12) * 360 - 90)

    # Calculate hand positions
    second_hand = (center + int(radius * 0.9 * cos(second_angle)),
                   center + int(radius * 0.9 * sin(second_angle)))
    minute_hand = (center + int(radius * 0.75 * cos(minute_angle)),
                   center + int(radius * 0.75 * sin(minute_angle)))
    hour_hand = (center + int(radius * 0.5 * cos(hour_angle)),
                 center + int(radius * 0.5 * sin(hour_angle)))

    # Draw hands
    draw.line([center, center, *second_hand], fill="red", width=2)
    draw.line([center, center, *minute_hand], fill="black", width=4)
    draw.line([center, center, *hour_hand], fill="black", width=6)

    # Display the clock
    image.show()

# Call the function to draw the clock
draw_clock()
