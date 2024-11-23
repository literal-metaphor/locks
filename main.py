import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import json
from random import choice

###################
# Initialize root #
###################
root = tk.Tk()

# Prevent interaction outside the lock screen
root.attributes('-fullscreen',True)
root.overrideredirect(True)

# Configure background
img = Image.open('assets/Background.png')
bg_img = ImageTk.PhotoImage(img)
cvs = tk.Canvas(root,
                width=0,
                height=0,
                highlightthickness=0,
                borderwidth=0)
cvs.pack(side=tk.TOP,
         fill=tk.BOTH,
         expand=True)
cvs.create_image(0,
                 0,
                 image=bg_img,
                 anchor=tk.NW)

# Create quit button
quitBtn = tk.Button(cvs,
                    text="Quit",
                    command=root.destroy)
quitBtn.pack(side=tk.TOP, anchor=tk.W)

# Track the date and time
def datetime_tracker():
  now = datetime.now()

  # Time
  current_time = now.strftime("%H:%M")
  cvs.delete("time_text")
  cvs.create_text(80,
                  440,
                  text=current_time,
                  fill="white",
                  font=('Inter 64'),
                  tag="time_text",
                  anchor=tk.W)

  # Date
  day_name = now.strftime("%A")
  month_name = now.strftime("%B")
  date = now.day

  cvs.delete("date_text")
  cvs.create_text(80,
                  520,
                  text=f"{day_name}, {month_name} {date}",
                  fill="white",
                  font=('Inter 32'),
                  tag="date_text",
                  anchor=tk.W)

  # Track every second
  root.after(1000, datetime_tracker)

def inspire():
  # Open quotes.json data
  f = open('assets/quotes.json')
  data = json.load(f)

  # Get random quote
  quote = choice(data["quotes"])

  # Display the selected data
  cvs.delete("quote_text")
  cvs.delete("author_text")
  cvs.create_text(80,
                  590,
                  text=f'"{quote["quote"]}"',
                  fill="white",
                  font=('Inter 16'),
                  tag="quote_text",
                  anchor=tk.W)
  cvs.create_text(80,
                  620,
                  text=f"- {quote["author"]}",
                  fill="white",
                  font=('Inter 13'),
                  tag="author_text",
                  anchor=tk.W)

  # Close the file
  f.close()

  # Change quote every 10 seconds
  root.after(10000, inspire)

# Call everything
datetime_tracker()
inspire()
#################################
# Initialize frame
frame = tk.Frame(root)
# Lock and loaded, let's do this!
root.mainloop()
