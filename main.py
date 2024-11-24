import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import json
from random import choice

# TODO: Specify name main thingy

###################
# Initialize root #
###################
root = tk.Tk()

# Prevent interaction outside the lock screen
root.attributes('-fullscreen',True)
root.overrideredirect(True)
# TODO: Prevent using Windows/Super key, Alt-F4, and other sneaky tactics
# * Suggestion: Create a whitelist system, don't allow any other input except A-B, a-z, 0-9, some special characters (like - and _), enter button, and mouse click

##################
# Define daemons #
##################
# Track the date and time
def clock_daemon():
  now = datetime.now()

  # Time
  current_time = now.strftime("%H:%M")
  frame.canvas.delete("time_text")
  frame.canvas.create_text(80,
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

  frame.canvas.delete("date_text")
  frame.canvas.create_text(80,
                  520,
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
  frame.canvas.create_text(80,
                  590,
                  text=f'"{quote["quote"]}"',
                  fill="white",
                  font=('Inter 16'),
                  tag="quote_text",
                  anchor=tk.W)
  frame.canvas.create_text(80,
                  620,
                  text=f"- {quote["author"]}",
                  fill="white",
                  font=('Inter 13'),
                  tag="author_text",
                  anchor=tk.W)

  # Close the file
  f.close()

  # Change quote every 10 seconds
  root.after(10000, inspire_daemon)

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
    clock_daemon()
    inspire_daemon()

# Initialize main frame
frame = Frame(root)
frame.pack(side=tk.TOP,
         fill=tk.BOTH,
         expand=True)

# Create quit button
quitBtn = tk.Button(frame.canvas,
                    text="Quit",
                    command=root.destroy)
quitBtn.pack(side=tk.TOP, anchor=tk.W)

# TODO: Click goes to sign in menu, with animation if possible
#################################
# Lock and loaded, let's do this!
root.mainloop()
