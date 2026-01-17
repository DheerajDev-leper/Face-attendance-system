from tkinter import *
from PIL import Image, ImageTk


class helper:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600+300+120")
        self.root.title("Help & Support")
        self.root.config(bg="#0f172a")
        self.root.resizable(False, False)

        # ---------- COLORS ----------
        self.CARD = "#020617"
        self.PRIMARY = "#2563eb"
        self.TEXT = "#e5e7eb"
        self.SUB = "#9ca3af"

        # ---------- TITLE ----------
        Label(
            self.root,
            text="Help & Support",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#0f172a"
        ).place(x=30, y=20)

        # ---------- CARD ----------
        card = Frame(self.root, bg=self.CARD, bd=0)
        card.place(x=60, y=90, width=780, height=460)

        # ---------- IMAGE ----------
        try:
            img = Image.open("logos/help.png")
            img = img.resize((170, 170), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
        except:
            self.photo = None

        Label(card, image=self.photo, bg=self.CARD).place(x=40, y=40)

        # ---------- SECTION TITLE ----------
        Label(
            card,
            text="Frequently Asked Questions",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.CARD
        ).place(x=240, y=40)

        # ---------- FAQ TEXT ----------
        faq = (
            "• How do I add a new student?\n"
            "  Go to Student Details → Fill form → Save.\n\n"
            "• How do I train the model?\n"
            "  Click Train Data → Wait until completed popup.\n\n"
            "• How to mark attendance automatically?\n"
            "  Open Face Detector → Detect Face → Attendance stored.\n\n"
            "• Why face not recognized?\n"
            "  → Ensure enough photos\n"
            "  → Proper lighting\n"
            "  → Face should be clear and visible\n"
        )

        Label(
            card,
            text=faq,
            font=("Segoe UI", 11),
            fg=self.TEXT,
            bg=self.CARD,
            justify=LEFT
        ).place(x=240, y=80)

        # ---------- CONTACT SUPPORT ----------
        Label(
            card,
            text="Contact Support",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.CARD
        ).place(x=40, y=260)

        support = (
            "📧 Email : support.attendance.ai@gmail.com\n"
            "📞 Phone : +91 XXXXX XXXXX\n"
            "⏱ Working Hours : 10:00 AM – 6:00 PM\n"
        )

        Label(
            card,
            text=support,
            font=("Segoe UI", 11),
            fg=self.TEXT,
            bg=self.CARD,
            justify=LEFT
        ).place(x=40, y=300)

        # ---------- CLOSE BUTTON ----------
        close_btn = Button(
            card,
            text="Close",
            font=("Segoe UI", 11, "bold"),
            bg=self.PRIMARY,
            fg="white",
            activebackground="#1e3a8a",
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.root.destroy
        )
        close_btn.place(x=650, y=400)

        # hover effect
        def on_enter(e): close_btn.config(bg="#1e3a8a")
        def on_leave(e): close_btn.config(bg=self.PRIMARY)

        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)


if __name__ == "__main__":
    root = Tk()
    obj = helper(root)
    root.mainloop()
