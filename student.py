from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
import cv2
import os
import re

from config import DB_CONFIG


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        # ================= VARIABLES =================
        self.var_dep = StringVar(value="Select Department")
        self.var_course = StringVar(value="Select Course")
        self.var_year = StringVar(value="Select Year")
        self.var_semester = StringVar(value="Select Semester")
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_gender = StringVar(value="Select Gender")
        self.var_dob = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio = StringVar(value="No")

        self.setup_ui()
        self.fetch_data()

    # ================= DATABASE =================
    def get_conn(self):
        return mysql.connector.connect(**DB_CONFIG)

    # ================= UI =================
    def setup_ui(self):
        header = Image.open("logos/image.png").resize((510, 130), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(header)
        for i in range(3):
            Label(self.root, image=self.header_photo).place(x=510 * i, y=0, width=510, height=130)

        bg = Image.open("logos/10450447.png").resize((1530, 660), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=130, width=1530, height=660)

        Label(bg_label, text="STUDENT MANAGEMENT SYSTEM",
              font=("times new roman", 35, "bold"),
              bg="white", fg="red").place(x=0, y=0, width=1530, height=50)

        main = Frame(bg_label, bg="white", bd=2)
        main.place(x=10, y=55, width=1510, height=595)

        self.build_left(main)
        self.build_right(main)

    # ================= LEFT PANEL =================
    def build_left(self, parent):
        left = LabelFrame(parent, text="Student Details",
                          font=("times new roman", 12, "bold"),
                          bg="white", bd=2, relief=RIDGE)
        left.place(x=10, y=10, width=740, height=570)

        frame = LabelFrame(left, text="Class Student Information",
                           font=("times new roman", 12, "bold"),
                           bg="white", bd=2, relief=RIDGE)
        frame.place(x=5, y=10, width=725, height=540)

        # ===== Comboboxes =====
        self.combo(frame, "Department", self.var_dep,
                   ("Select Department", "Computer", "IT", "ENTC", "Mechanical"), 0, 0)
        self.combo(frame, "Course", self.var_course,
                   ("Select Course", "FE", "SE", "TE", "BE"), 0, 2)
        self.combo(frame, "Year", self.var_year,
                   ("Select Year", "2021-22", "2022-23", "2023-24"), 1, 0)
        self.combo(frame, "Semester", self.var_semester,
                   ("Select Semester", "Semester 1", "Semester 2"), 1, 2)

        # ===== Entries =====
        self.entry(frame, "Student ID", self.var_std_id, 2, 0)
        self.entry(frame, "Name", self.var_std_name, 2, 2)
        self.entry(frame, "Division", self.var_div, 3, 0)
        self.entry(frame, "Roll No", self.var_roll, 3, 2)
        self.entry(frame, "DOB (DD/MM/YYYY)", self.var_dob, 4, 0)
        self.entry(frame, "Email", self.var_email, 4, 2)
        self.entry(frame, "Phone", self.var_phone, 5, 0)
        self.entry(frame, "Address", self.var_address, 5, 2)
        self.entry(frame, "Teacher", self.var_teacher, 6, 0)

        self.combo(frame, "Gender", self.var_gender,
                   ("Select Gender", "Male", "Female", "Other"), 6, 2)

        # ===== Radio =====
        Radiobutton(frame, text="Take Photo Sample", variable=self.var_radio,
                    value="Yes", bg="white").place(x=5, y=300)
        Radiobutton(frame, text="No Photo Sample", variable=self.var_radio,
                    value="No", bg="white").place(x=180, y=300)

        # ===== Buttons =====
        btn = Frame(frame, bg="white")
        btn.place(x=5, y=330, width=700, height=120)

        Button(btn, text="Save", width=15, command=self.add_data,
               bg="blue", fg="white").grid(row=0, column=0, padx=5)
        Button(btn, text="Update", width=15, command=self.update_data,
               bg="blue", fg="white").grid(row=0, column=1, padx=5)
        Button(btn, text="Delete", width=15, command=self.delete_data,
               bg="blue", fg="white").grid(row=0, column=2, padx=5)
        Button(btn, text="Reset", width=15, command=self.reset_data,
               bg="blue", fg="white").grid(row=0, column=3, padx=5)

        Button(btn, text="TAKE PHOTO SAMPLE",
               width=35, command=self.generate_data,
               bg="green", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

    # ================= RIGHT PANEL =================
    def build_right(self, parent):
        right = LabelFrame(parent, text="Student Database",
                           font=("times new roman", 12, "bold"),
                           bg="white", bd=2, relief=RIDGE)
        right.place(x=760, y=10, width=740, height=570)

        frame = Frame(right, bg="white")
        frame.place(x=5, y=5, width=725, height=550)

        scroll_y = ttk.Scrollbar(frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.student_table = ttk.Treeview(
            frame,
            columns=(
                "id","student_id","department","course","year","semester",
                "name","division","roll","gender","dob",
                "email","phone","address","teacher","photo"
            ),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.student_table.yview)

        for col in self.student_table["columns"]:
            self.student_table.heading(col, text=col.upper())
            self.student_table.column(col, width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

    # ================= HELPERS =================
    def combo(self, parent, text, var, values, r, c):
        Label(parent, text=text, bg="white").grid(row=r, column=c, sticky=W, padx=5, pady=5)
        ttk.Combobox(parent, textvariable=var, values=values,
                     state="readonly", width=18).grid(row=r, column=c+1, padx=5)

    def entry(self, parent, text, var, r, c):
        Label(parent, text=text, bg="white").grid(row=r, column=c, sticky=W, padx=5, pady=5)
        ttk.Entry(parent, textvariable=var, width=20).grid(row=r, column=c+1, padx=5)

    # ================= VALIDATION =================
    def validate_inputs(self):
        if not self.var_std_id.get():
            return "Student ID required"
        if self.var_gender.get() == "Select Gender":
            return "Select Gender"
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", self.var_dob.get()):
            return "DOB must be DD/MM/YYYY"
        if not re.fullmatch(r"\d{10}", self.var_phone.get()):
            return "Phone must be 10 digits"
        return None

    # ================= CRUD =================
    def add_data(self):
        error = self.validate_inputs()
        if error:
            messagebox.showerror("Error", error)
            return

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO student VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            self.var_std_id.get(), self.var_dep.get(), self.var_course.get(),
            self.var_year.get(), self.var_semester.get(),
            self.var_std_name.get(), self.var_div.get(), self.var_roll.get(),
            self.var_gender.get(), self.var_dob.get(), self.var_email.get(),
            self.var_phone.get(), self.var_address.get(),
            self.var_teacher.get(), self.var_radio.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()

    def fetch_data(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        self.student_table.delete(*self.student_table.get_children())
        for row in cur.fetchall():
            self.student_table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, _):
        row = self.student_table.item(self.student_table.focus())["values"]
        if row:
            (
                _, self.var_std_id.set(row[1]), self.var_dep.set(row[2]),
                self.var_course.set(row[3]), self.var_year.set(row[4]),
                self.var_semester.set(row[5]), self.var_std_name.set(row[6]),
                self.var_div.set(row[7]), self.var_roll.set(row[8]),
                self.var_gender.set(row[9]), self.var_dob.set(row[10]),
                self.var_email.set(row[11]), self.var_phone.set(row[12]),
                self.var_address.set(row[13]), self.var_teacher.set(row[14]),
                self.var_radio.set(row[15])
            )

    def update_data(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE student SET
        department=%s, course=%s, year=%s, semester=%s, name=%s,
        division=%s, roll_no=%s, gender=%s, dob=%s, email=%s,
        phone=%s, address=%s, teacher=%s, photo_sample=%s
        WHERE student_id=%s
        """, (
            self.var_dep.get(), self.var_course.get(), self.var_year.get(),
            self.var_semester.get(), self.var_std_name.get(), self.var_div.get(),
            self.var_roll.get(), self.var_gender.get(), self.var_dob.get(),
            self.var_email.get(), self.var_phone.get(), self.var_address.get(),
            self.var_teacher.get(), self.var_radio.get(), self.var_std_id.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()

    def delete_data(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE student_id=%s", (self.var_std_id.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()

    # ================= FACE DATA =================
    def generate_data(self):
        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        img_id = 0
        os.makedirs("data", exist_ok=True)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                img_id += 1
                face = cv2.resize(gray[y:y+h, x:x+w], (450, 450))
                cv2.imwrite(f"data/user.{self.var_std_id.get()}.{img_id}.jpg", face)
                cv2.imshow("Capturing Faces", face)

            if cv2.waitKey(1) == 13 or img_id == 100:
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Face samples generated successfully")

    def reset_data(self):
        for var in [
            self.var_dep, self.var_course, self.var_year, self.var_semester,
            self.var_std_id, self.var_std_name, self.var_div,
            self.var_roll, self.var_gender, self.var_dob,
            self.var_email, self.var_phone, self.var_address,
            self.var_teacher
        ]:
            var.set("")
        self.var_radio.set("No")


if __name__ == "__main__":
    root = Tk()
    Student(root)
    root.mainloop()
