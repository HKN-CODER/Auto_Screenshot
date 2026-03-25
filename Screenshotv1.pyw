import mss
import os
import time
import threading
from datetime import datetime
from PIL import Image
import numpy as np
import tkinter as tk

# Default save path
pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
today_folder = datetime.now().strftime("%Y-%m-%d")
base_folder = os.path.join(pictures_path, today_folder)

os.makedirs(base_folder, exist_ok=True)

running = True

def convert_to_24(hour, minute, ampm):
    hour = int(hour)
    if ampm == "PM" and hour != 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0
    return hour, int(minute)

def capture_loop():

    count = 0

    with mss.mss() as sct:

        monitor_count = len(sct.monitors) - 1

        for i in range(1, monitor_count + 1):
            os.makedirs(os.path.join(base_folder, f"screen{i}"), exist_ok=True)

        while running:

            now = datetime.now()

            sh, sm = convert_to_24(start_hour.get(), start_min.get(), start_ampm.get())
            eh, em = convert_to_24(end_hour.get(), end_min.get(), end_ampm.get())

            start_time = now.replace(hour=sh, minute=sm, second=0)
            end_time = now.replace(hour=eh, minute=em, second=59)

            interval = int(seconds_var.get())

            if start_time <= now <= end_time:

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                saved_this_cycle = 0

                for i, monitor in enumerate(sct.monitors[1:], start=1):

                    folder = os.path.join(base_folder, f"screen{i}")
                    filename = f"screen{i}_{timestamp}.jpg"
                    path = os.path.join(folder, filename)

                    screenshot = sct.grab(monitor)
                    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

                    img_array = np.array(img)

                    # Check if black screen
                    if img_array.mean() < 5 and not save_black_var.get():
                        status_label.config(
                            text=f"Screen{i} black → skipped"
                        )
                        continue

                    img.save(path, "JPEG")
                    saved_this_cycle += 1

                if saved_this_cycle > 0:
                    count += 1
                    status_label.config(
                        text=f"Capturing... Cycle {count} | {timestamp}"
                    )
                else:
                    status_label.config(
                        text=f"All screens black/off → skipped {timestamp}"
                    )

            else:
                status_label.config(
                    text=f"Waiting for schedule | {now.strftime('%I:%M:%S %p')}"
                )

            time.sleep(interval)

# GUI
root = tk.Tk()
root.title("Screen Capture Monitor")
root.geometry("500x360")

hours = [f"{i:02d}" for i in range(1,13)]
minutes = [f"{i:02d}" for i in range(60)]

# Start time
tk.Label(root,text="Start Time").pack()

frame1 = tk.Frame(root)
frame1.pack()

start_hour = tk.StringVar(value="09")
start_min = tk.StringVar(value="00")
start_ampm = tk.StringVar(value="AM")

tk.OptionMenu(frame1,start_hour,*hours).pack(side="left")
tk.Label(frame1,text=":").pack(side="left")
tk.OptionMenu(frame1,start_min,*minutes).pack(side="left")
tk.OptionMenu(frame1,start_ampm,"AM","PM").pack(side="left")

# End time
tk.Label(root,text="End Time").pack()

frame2 = tk.Frame(root)
frame2.pack()

end_hour = tk.StringVar(value="03")
end_min = tk.StringVar(value="30")
end_ampm = tk.StringVar(value="PM")

tk.OptionMenu(frame2,end_hour,*hours).pack(side="left")
tk.Label(frame2,text=":").pack(side="left")
tk.OptionMenu(frame2,end_min,*minutes).pack(side="left")
tk.OptionMenu(frame2,end_ampm,"AM","PM").pack(side="left")

# Interval
tk.Label(root,text="Capture Interval (seconds)").pack()

seconds_var = tk.StringVar(value="5")
tk.Entry(root,textvariable=seconds_var,width=10).pack()

# Checkbox for black screen
save_black_var = tk.BooleanVar(value=False)

tk.Checkbutton(
    root,
    text="Save black screen images",
    variable=save_black_var
).pack(pady=5)

# Save path display
tk.Label(root,text="Save Path",font=("Arial",10,"bold")).pack(pady=5)

path_label = tk.Label(root,text=base_folder,wraplength=460,fg="blue")
path_label.pack()

# Status
status_label = tk.Label(root,text="Starting monitor...",wraplength=460)
status_label.pack(pady=10)

# Start capture automatically
threading.Thread(target=capture_loop,daemon=True).start()

root.mainloop()