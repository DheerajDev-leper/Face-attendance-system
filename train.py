from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        # ================= TITLE =================
        Label(
            self.root,
            text="TRAIN DATA SET",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="blue"
        ).place(x=0, y=0, width=1530, height=45)

        # ================= TOP IMAGE =================
        img_top = Image.open(r"logos\training.png").resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        Label(self.root, image=self.photoimg_top).place(x=0, y=45, width=1530, height=325)

        # ================= TRAIN BUTTON =================
        Button(
            self.root,
            text="TRAIN DATA",
            cursor="hand2",
            command=self.train_classifier,
            font=("times new roman", 30, "bold"),
            bg="blue",
            fg="white"
        ).place(x=0, y=350, width=1530, height=70)

        # ================= BOTTOM IMAGE =================
        img_bottom = Image.open(r"logos\training.png").resize((1530, 380), Image.Resampling.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        Label(self.root, image=self.photoimg_bottom).place(x=0, y=410, width=1530, height=380)

    # ================= TRAINING =================
    def train_classifier(self):
        data_dir = "data"

        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data folder not found.\nCapture face samples first.")
            return

        image_files = [
            os.path.join(data_dir, f)
            for f in os.listdir(data_dir)
            if f.endswith(".jpg")
        ]

        if not image_files:
            messagebox.showerror("Error", "No training images found in data folder.")
            return

        faces = []
        ids = []

        for image_path in image_files:
            try:
                img = Image.open(image_path).convert("L")
                image_np = np.array(img, "uint8")

                # filename format: user.<id>.<img_id>.jpg
                filename = os.path.basename(image_path)
                student_id = int(filename.split(".")[1])

                faces.append(image_np)
                ids.append(student_id)

            except Exception as e:
                print(f"Skipping file {image_path}: {e}")

        if not faces:
            messagebox.showerror("Error", "No valid face images found.")
            return

        ids = np.array(ids)

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, ids)
            recognizer.write("classifier.xml")

            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Training completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Training failed:\n{str(e)}")


if __name__ == "__main__":
    root = Tk()
    Train(root)
    root.mainloop()
