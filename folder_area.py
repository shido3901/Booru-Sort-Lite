import tkinter as tk
import time
from tag import create_tag_window

def create_folder_area(parent):
    folder_area = tk.Frame(parent, bg="#242323", width=1600, height=1080)
    folder_area.grid(row=0, column=1, rowspan=6, sticky="nsew")

    folder_area.grid_rowconfigure(0, weight=1)
    folder_area.grid_columnconfigure(0, weight=1)
    
    global right_click_menu
    right_click_menu = tk.Menu(parent, tearoff=0, bg="#333333", fg="white", activebackground="#555555", activeforeground="cyan", font=("Arial", 10))
    right_click_menu.config(bg="#171717", bd=0, relief="flat")

    right_click_menu.add_command(label="View", command=create_tag_window)
    right_click_menu.add_separator()
    right_click_menu.add_command(label="New Folder", command=create_tag_window)
    right_click_menu.add_separator()
    right_click_menu.add_command(label="New tag", command=lambda: create_tag_window(parent))

    return folder_area


def folder_area_right_click(event):
        global right_click_menu
        if right_click_menu:
            right_click_menu.tk_popup(event.x_root, event.y_root)

##folder_right_click = tk.Menu(create_folder_area, tearoff=0)
##folder_right_click.add_command(label="View", command=create_tag_window)
##folder_right_click.add_separator()
##folder_right_click.add_command(label="Delete Folder", command=create_tag_window)
##folder_right_click.add_separator()
##folder_right_click.add_command(label="New tag", command=create_tag_window)

class SelectBox:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left_click_hold = False
        self.rect = None
        self.x_start = None
        self.y_start = None
        self.last_motion_time = 0
        self.throttle_delay = 0.016

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<ButtonRelease-1>", self.left_click_release)
        self.canvas.bind("<Motion>", self.mouse_move)

    def left_click(self, event):
        self.on_left_click_press(event)
    
    def left_click_release(self, event):
        self.on_left_click_release(event)

    def on_left_click_press(self, event):
        self.left_click_hold = True
        self.x_start = event.x
        self.y_start = event.y

        if self.rect is None:
            self.rect = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_start, self.y_start, outline="#27bde7", width=1.5)

    def on_left_click_release(self, event):
        self.left_click_hold = False
        if self.rect:
            self.canvas.coords(self.rect, 0, 0, 0, 0)

    def mouse_move(self, event):
        now = time.time()
        if now - self.last_motion_time < self.throttle_delay:
            return
        self.last_motion_time = now

        if self.left_click_hold and self.rect:
            self.canvas.coords(self.rect, self.x_start, self.y_start, event.x, event.y)


