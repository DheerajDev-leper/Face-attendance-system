from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from datetime import datetime
import threading

from config import DB_CONFIG


class face_recog:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        # ===== Thread control =====
        self.running = False
        self.threshold = 75  # accuracy threshold %

        # ===== Title =====
        Label(
            self.root, text="FACE RECOGNITION",
            font=("times new roman", 35, "bold"),
            bg="white", fg="blue"
        ).place(x=0, y=0, width=1530, height=45)

        # ===== Images =====
        left_img = Image.open(r"logos\detector.png").resize((650, 750), Image.Resampling.LANCZOS)
        self.left_photo = ImageTk.PhotoImage(left_img)
        Label(self.root, image=self.left_photo).place(x=0, y=45, width=650, height=750)

        right_img = Image.open(r"logos\face_detect.png").resize((880, 750), Image.Resampling.LANCZOS)
        self.right_photo = ImageTk.PhotoImage(right_img)
        self.right_label = Label(self.root, image=self.right_photo)
        self.right_label.place(x=650, y=45, width=880, height=750)

        # ===== Detect Button =====
        Button(
            self.right_label,
            text="DETECT FACE",
            command=self.start_face_recognition,
            cursor="hand2",
            font=("times new roman", 30, "bold"),
            bg="blue", fg="white"
        ).place(x=350, y=350, width=400, height=70)

        # ===== Accuracy Label =====
        self.acc_label = Label(
            self.right_label,
            text="Accuracy: -- %",
            font=("times new roman", 18, "bold"),
            bg="white", fg="green"
        )
        self.acc_label.place(x=360, y=440)

        self.root.protocol("WM_DELETE_WINDOW", self.stop_camera)

    # ================= DATABASE =================
    def load_students(self):
        conn = mysql.connector.connect(**DB_CONFIG)

        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, roll_no, department FROM student")
        data = {row[0]: row[1:] for row in cursor.fetchall()}
        conn.close()
        return data

    # ================= ATTENDANCE =================
    def mark_attendance(self, sid, roll, name, dept):
        today = datetime.now().strftime("%d/%m/%Y")

        if not os.path.exists("Attendance.csv"):
            with open("Attendance.csv", "w") as f:
                f.write("ID,Roll,Name,Department,Time,Date,Status")

        with open("Attendance.csv", "r+") as f:
            for line in f.readlines():
                entry = line.split(",")
                if entry[0] == str(sid) and entry[5] == today:
                    return

            now = datetime.now()
            f.write(
                f"\n{sid},{roll},{name},{dept},"
                f"{now.strftime('%H:%M:%S')},{today},Present"
            )

    # ================= THREAD START =================
    def start_face_recognition(self):
        if self.running:
            return

        threading.Thread(
            target=self.face_recognition,
            daemon=True
        ).start()

    # ================= FACE RECOGNITION =================
    def face_recognition(self):
        if not os.path.exists("classifier.xml"):
            messagebox.showerror("Error", "Classifier not found. Train model first.")
            return

        students = self.load_students()
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("classifier.xml")

        cap = cv2.VideoCapture(0)
        self.running = True

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 10)

            for (x, y, w, h) in faces:
                sid, distance = recognizer.predict(gray[y:y+h, x:x+w])

                # ===== Accuracy Calculation =====
                accuracy = max(0, min(100, 100 - int(distance)))
                self.acc_label.config(text=f"Accuracy: {accuracy}%")

                if accuracy >= self.threshold and sid in students:
                    name, roll, dept = students[sid]

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name}", (x, y-40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(frame, f"Accuracy: {accuracy}%", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                    self.mark_attendance(sid, roll, name, dept)

                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown Face", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) == 13:  # ENTER key
                break

        cap.release()
        cv2.destroyAllWindows()
        self.running = False
        self.acc_label.config(text="Accuracy: -- %")

    # ================= SAFE EXIT =================
    def stop_camera(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    face_recog(root)
    root.mainloop()
