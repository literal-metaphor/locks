import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import json
from random import choice
from keyboard import block_key

# TODO: Specify name main thingy

###################
# Initialize root #
###################
root = tk.Tk()
root.title("locks")

# Prevent interaction outside the lock screen
# Focus fullscreen with no border
root.wm_attributes('-fullscreen',True)
# Force always on top of other app
root.wm_attributes("-topmost", True)
root.overrideredirect(True)
root.grab_set()

# Prevent closing externally
def on_closing():
  pass
root.protocol("WM_DELETE_WINDOW", on_closing)

# Block some keys
for key in ['esc', 'tab', 'ctrl', 'alt', 'win', 'del'] + [f'f{i}' for i in range(1, 13)]:
  block_key(key)

# Always focus on lock screen
def keep_focus():
  root.lift()
  root.after(100, keep_focus)
keep_focus()

# ! There's no way to prevent Ctrl+Alt+Del without altering the underlying Windows system as it is undeniably crucial to mitigate crash and other fatal error, or just access task manager

# Custom frame for optimized background
class Frame(tk.Frame):
  def __init__(self, master, *pargs):
    tk.Frame.__init__(self, master, *pargs)

    # Open the background and make a copy for virtualized interaction
    self.img = Image.open("assets/Background.png")
    self.img_copy = self.img.copy()
    self.bg_img = ImageTk.PhotoImage(self.img)

    # Create a canvas inside the frame for basically what most of the app would be using
    self.canvas = tk.Canvas(self,
                            width=0,
                            height=0,
                            highlightthickness=0,
                            borderwidth=0)
    self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    self.canvas.bind('<Configure>', self.configure)

  def configure(self, event):
    # Resize the background image to fit the window size
    self.img = self.img_copy.resize((event.width, event.height))
    self.bg_img = ImageTk.PhotoImage(self.img)
    # Add the background to canvas
    self.canvas.create_image(0,
                             0,
                             image=self.bg_img,
                             anchor=tk.NW)

    # Call the trackers
    fix_coordinaates()
    init_daemon()

# Initialize main frame
frame = Frame(root)
frame.pack(side=tk.TOP,
         fill=tk.BOTH,
         expand=True)

##################
# Define daemons #
##################
# Hacky way, but it's easy - Base some coordinates on other's absolute coordinates
time_x = None
time_y = None
date_x = None
date_y = None
quote_x = None
quote_y = None
author_x = None
author_y = None

# Fix the actual coordinates after initial rendering
def fix_coordinaates():
  global time_x
  global time_y
  global date_x
  global date_y
  global quote_x
  global quote_y
  global author_x
  global author_y

  time_x = frame.canvas.winfo_width() * 0.08
  time_y = frame.canvas.winfo_height() * 0.6
  date_x = time_x + 10
  date_y = time_y + 80
  quote_x = date_x
  quote_y = date_y + 80
  author_x = quote_x
  author_y = quote_y + 40

def init_daemon():
  clock_daemon()
  inspire_daemon()

# Track the date and time
def clock_daemon():
  now = datetime.now()

  # Time
  current_time = now.strftime("%H:%M")

  frame.canvas.delete("time_text")
  frame.canvas.create_text(time_x,
                  time_y,
                  text=current_time,
                  fill="white",
                  font=('Inter 64'),
                  tag="time_text",
                  anchor=tk.W)

  # Date
  day_name = now.strftime("%A")
  month_name = now.strftime("%B")
  date = now.day

  frame.canvas.delete("date_text")
  frame.canvas.create_text(date_x,
                  date_y,
                  text=f"{day_name}, {month_name} {date}",
                  fill="white",
                  font=('Inter 32'),
                  tag="date_text",
                  anchor=tk.W)

  # Track every second
  root.after(1000, clock_daemon)

# TODO: Add fading-in and out animation (if possible)
def inspire_daemon():
  # Open quotes.json data
  f = open('assets/quotes.json')
  data = json.load(f)

  # Get random quote
  quote = choice(data["quotes"])

  # Display the selected data
  frame.canvas.delete("quote_text")
  frame.canvas.delete("author_text")

  frame.canvas.create_text(quote_x,
                            quote_y,
                            text=f'"{quote["quote"]}"',
                            fill="white",
                            font=('Inter', 16),
                            tag="quote_text",
                            anchor=tk.W)
  frame.canvas.create_text(author_x,
                            author_y,
                            text=f"- {quote['author']}",
                            fill="white",
                            font=('Inter', 13),
                            tag="author_text",
                            anchor=tk.W)

  # Close the file
  f.close()

  # Change quote every 10 seconds
  root.after(10000, inspire_daemon)

# Create quit button
quitBtn = tk.Button(frame.canvas,
                    text="Quit",
                    command=root.destroy)
quitBtn.pack(side=tk.TOP, anchor=tk.W)

# TODO: Click goes to sign in menu, with animation if possible
#################################
# Lock and loaded, let's do this!
root.mainloop()
