import tkinter as tk
import time
import math
from PIL import Image, ImageDraw, ImageTk

def update_clock():
    current_time = time.localtime()
    hour = current_time.tm_hour % 12  # 12-hour format
    minute = current_time.tm_min
    second = current_time.tm_sec

    # Create a blank image
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    # Clock face
    draw.ellipse((10, 10, 290, 290), outline="black", width=2)

    # Center point
    center_x = 150
    center_y = 150
    draw.ellipse((center_x - 5, center_y - 5, center_x + 5, center_y + 5), fill="black")

    # Hour hand
    hour_angle = math.radians((hour * 30) + (minute / 2) - 90)  # Adjust for starting at 12
    hour_x = center_x + 80 * math.cos(hour_angle)
    hour_y = center_y + 80 * math.sin(hour_angle)
    draw.line((center_x, center_y, hour_x, hour_y), fill="black", width=4)

    # Minute hand
    minute_angle = math.radians((minute * 6) - 90)
    minute_x = center_x + 110 * math.cos(minute_angle)
    minute_y = center_y + 110 * math.sin(minute_angle)
    draw.line((center_x, center_y, minute_x, minute_y), fill="black", width=3)

    # Second hand
    second_angle = math.radians((second * 6) - 90)
    second_x = center_x + 130 * math.cos(second_angle)
    second_y = center_y + 130 * math.sin(second_angle)
    draw.line((center_x, center_y, second_x, second_y), fill="red", width=1)

    #Update the Tkinter Label
    global photo #Make photo global so it is not garbage collected
    photo = ImageTk.PhotoImage(img)
    clock_label.config(image=photo)
    clock_label.after(1000, update_clock) #Update every second


# Create the main window
root = tk.Tk()
root.title("Analog Clock")

#Create a Label to hold the clock image
clock_label = tk.Label(root)
clock_label.pack()

#Start the clock
update_clock()

root.mainloop()

