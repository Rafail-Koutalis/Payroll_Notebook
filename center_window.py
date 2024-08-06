from tkinter import END
from sys import exit
def center_window(root, width, height):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window
    root.geometry(f'{width}x{height}+{x}+{y}')


def entry_clear(*args,entry_1) :
    for entry in args :
        entry.delete(0,END)
    entry_1.focus()

def forget_all(root) :
    for widget in root.winfo_children() :
        widget.grid_forget()

def root_config(new_root,color,title,width,height) :
    center_window(new_root,width,height)
    new_root.title(title)
    new_root.configure(bg=color)
    new_root.focus_force()


def bind_escape(event) :
    exit()