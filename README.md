# 🎓 Face Recognition Attendance System

A desktop-based **Face Recognition Attendance System** built with **Python, OpenCV, Tkinter, and MySQL**. It automates student attendance by detecting and recognizing faces in real time through a webcam — no more manual roll calls, no more proxy attendance.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-LBPH-green?logo=opencv&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-yellow)

---

## 📌 Features

- 📝 **Student Registration** — capture ID, name, department, gender, and other profile details
- 📷 **Face Dataset Generation** — capture multiple face samples per student via webcam
- 🧠 **Model Training** — train an LBPH (Local Binary Patterns Histograms) face recognizer on the dataset
- 🎯 **Real-Time Recognition** — detect and recognize faces live and mark attendance automatically
- 📊 **Attendance Management** — attendance records are logged and stored for easy retrieval
- 🖥️ **User-Friendly GUI** — simple Tkinter-based desktop interface
- 🔐 **MySQL Integration** — secure, persistent storage of student and attendance data

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Face Detection | OpenCV Haar Cascade (`haarcascade_frontalface_default.xml`) |
| Face Recognition | OpenCV LBPH Algorithm |
| GUI | Tkinter |
| Database | MySQL |
| Image Processing | NumPy, Pillow (PIL) |

---

## 📂 Project Structure

```
Face-attendance-system/
├── logos/                              # App logos/branding assets
├── main.py                             # Application entry point / main GUI window
├── student.py                          # Student registration module
├── face_recog.py                       # Real-time face detection & recognition logic
├── train.py                            # Trains the LBPH model on captured face data
├── attendance.py                       # Attendance marking & record handling
├── helper.py                           # Shared utility/helper functions
├── developer.py                        # Developer/about info window
├── config.py                           # MySQL database configuration
├── classifier.xml                      # Trained LBPH face recognition model
├── haarcascade_frontalface_default.xml # Pretrained Haar Cascade for face detection
└── README.md
```

---

## 🧠 How It Works

1. **Register Student** — Add student details (ID, name, department, gender, etc.) through the GUI.
2. **Generate Face Dataset** — Capture multiple face samples of the student using the webcam.
3. **Train Model** — Train the LBPH face recognition model on the captured dataset (`train.py`), producing `classifier.xml`.
4. **Recognize Face & Mark Attendance** — The webcam feed is scanned in real time; recognized faces are automatically marked present in the database.
5. **View Attendance Records** — Attendance data is stored in MySQL and can be reviewed/managed at any time.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/DheerajDev-leper/Face-attendance-system.git
cd Face-attendance-system
```

### 2️⃣ Install Required Libraries

```bash
pip install opencv-python opencv-contrib-python mysql-connector-python pillow numpy
```

> `opencv-contrib-python` is required for the LBPH face recognizer (`cv2.face`).

### 3️⃣ Set Up MySQL

Create a database (matching the name in `config.py`, e.g. `face_recog`):

```sql
CREATE DATABASE face_recog;
```

### 4️⃣ Configure Database Credentials

Update `config.py` with your local MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password_here",
    "database": "face_recog"
}
```

### 5️⃣ Run the Application

```bash
python main.py
```

---

## ▶️ Usage

1. Launch the app with `python main.py`.
2. Go to **Student Registration** and add a new student's details.
3. Use **Generate Dataset** to capture face samples via webcam.
4. Run **Train Model** to update the LBPH classifier with the new data.
5. Open **Face Recognition / Attendance** to start real-time detection — attendance is marked automatically when a registered face is recognized.
6. Check the **Attendance Records** section for logs.

---

## ⚠️ Notes & Requirements

- A working **webcam** is required for dataset capture and live recognition.
- **MySQL Server** must be installed and running locally (or update `config.py` to point to a remote instance).
- Recognition accuracy improves with more/better-quality face samples per student and consistent lighting conditions.
- Tested with Python 3.x on Windows/Linux.

---



## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo, open issues, or submit pull requests to improve functionality, fix bugs, or enhance documentation.

## 👤 Author

**DheerajDev-leper** — [GitHub Profile](https://github.com/DheerajDev-leper)
