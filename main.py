from tkinter import *
from tkinter import messagebox
import tkinter
from PIL import Image, ImageTk
import os

from student import Student
from train import Train
from face_recog import face_recog
from attendance import Attendance
from developer import developer
from helper import helper


class Face_RecognitionApp:
    # ================= CONFIG =================
    WIDTH = 1530
    HEIGHT = 790

    BTN_BG = "#003d82"
    BTN_HOVER = "#0056b3"
    BTN_ACTIVE = "#004494"

    TITLE_BG = "white"
    TITLE_FG = "red"

    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+0+0")
        self.root.title("Face Recognition Attendance System")
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap("logos/icon.ico")
        except:
            pass

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logos_dir = os.path.join(self.base_dir, "logos")
        os.makedirs(self.logos_dir, exist_ok=True)

        self.images = {}  # prevent garbage collection
        self.setup_ui()

    # ================= UI =================
    def setup_ui(self):
        self.setup_header()
        self.setup_background()
        self.setup_buttons()

    def load_image(self, name, size):
        try:
            path = os.path.join(self.logos_dir, name)
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        except:
            img = Image.new("RGB", size, "#cccccc")
        photo = ImageTk.PhotoImage(img)
        self.images[name] = photo
        return photo

    def setup_header(self):
        img = self.load_image("image.png", (510, 130))
        for i in range(3):
            Label(self.root, image=img).place(x=510*i, y=0, width=510, height=130)

    def setup_background(self):
        bg = self.load_image("10450447.png", (1530, 660))
        self.bg_label = Label(self.root, image=bg)
        self.bg_label.place(x=0, y=130, width=1530, height=660)

        Label(
            self.bg_label,
            text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",
            font=("times new roman", 35, "bold"),
            bg=self.TITLE_BG,
            fg=self.TITLE_FG
        ).place(x=0, y=0, width=1530, height=45)

    # ================= BUTTONS =================
    def setup_buttons(self):
        buttons = [
            ("students.png", "Student Details", self.student_details, 100, 90),
            ("detector.png", "Face Detector", self.open_face_recog, 460, 90),
            ("attendance.png", "Attendance", self.open_attendance, 820, 90),
            ("help.png", "Help Desk", self.open_helper, 1180, 90),
            ("train.png", "Train Data", self.open_train, 100, 400),
            ("photos.png", "Photos", self.open_img, 460, 400),
            ("developer.png", "Developer", self.open_developer, 820, 400),
            ("exit.png", "Exit", self.exit_app, 1180, 400),
        ]

        for img, text, cmd, x, y in buttons:
            self.create_button(img, text, cmd, x, y)

    def create_button(self, img_name, text, command, x, y):
        img = self.load_image(img_name, (220, 200))
        Button(
            self.bg_label, image=img, command=command,
            cursor="hand2", borderwidth=0,
            bg=self.bg_label["bg"], activebackground=self.bg_label["bg"]
        ).place(x=x, y=y, width=220, height=200)

        btn = Button(
            self.bg_label, text=text, command=command,
            font=("times new roman", 15, "bold"),
            bg=self.BTN_BG, fg="white",
            activebackground=self.BTN_ACTIVE,
            cursor="hand2", borderwidth=0
        )
        btn.place(x=x, y=y+210, width=220, height=40)
        self.add_hover(btn)

    # ================= NAVIGATION =================
    def open_new_window(self, cls):
        win = Toplevel(self.root)
        cls(win)

    def student_details(self):
        self.open_new_window(Student)

    def open_face_recog(self):
        self.open_new_window(face_recog)

    def open_attendance(self):
        self.open_new_window(Attendance)

    def open_train(self):
        self.open_new_window(Train)

    def open_developer(self):
        self.open_new_window(developer)

    def open_helper(self):
        self.open_new_window(helper)

    def open_img(self):
        folder = os.path.join(self.base_dir, "data")
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showerror("Error", "Data folder not found")

    # ================= UTIL =================
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

    def add_hover(self, btn):
        btn.bind("<Enter>", lambda e: e.widget.config(bg=self.BTN_HOVER))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=self.BTN_BG))


if __name__ == "__main__":
    root = Tk()
    Face_RecognitionApp(root)
    root.mainloop()
