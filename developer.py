from tkinter import *
from PIL import Image, ImageTk


class developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        self._create_header()
        self._create_background()
        self._create_profile_card()

    # ================= HEADER =================
    def _create_header(self):
        Label(
            self.root,
            text="FACE RECOGNITION",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="blue"
        ).place(x=0, y=0, width=1530, height=45)

    # ================= BACKGROUND =================
    def _create_background(self):
        img = Image.open(r"logos\detector.png")
        img = img.resize((1530, 750), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)

        Label(self.root, image=self.bg_photo).place(x=0, y=45, width=1530, height=750)

    # ================= PROFILE CARD =================
    def _create_profile_card(self):
        card = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        card.place(x=980, y=90, width=520, height=300)

        Label(
            card, text="Hello 👋",
            font=("times new roman", 22, "bold"),
            bg="white", fg="green"
        ).pack(pady=(20, 5))

        Label(
            card, text="I'm Dheeraj Malviya",
            font=("times new roman", 20, "bold"),
            bg="white"
        ).pack(pady=5)

        ttk_line = Frame(card, bg="gray", height=2)
        ttk_line.pack(fill=X, padx=40, pady=10)

        Label(
            card, text="Python Developer",
            font=("times new roman", 14, "bold"),
            bg="white", fg="blue"
        ).pack(pady=5)

        Label(
            card, text="Face Recognition | AI | ML",
            font=("times new roman", 12),
            bg="white"
        ).pack(pady=5)

        Label(
            card, text="Final Year Engineering Project",
            font=("times new roman", 11, "italic"),
            bg="white", fg="gray"
        ).pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    developer(root)
    root.mainloop()
