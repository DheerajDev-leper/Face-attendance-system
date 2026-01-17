from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        # ================= VARIABLES =================
        self.var_att_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dep = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_status = StringVar(value="Status")

        self.data = []

        self._set_current_datetime()
        self._load_ui()

    # ================= UI SETUP =================
    def _load_ui(self):
        self._load_header()
        self._load_background()
        self._load_frames()
        self._load_table()

    def _load_header(self):
        img = Image.open(r"logos\image.png").resize((510, 130), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(img)

        for i in range(3):
            Label(self.root, image=self.header_photo).place(x=510 * i, y=0, width=510, height=130)

    def _load_background(self):
        bg = Image.open(r"logos\10450447.png").resize((1530, 660), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg)

        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=130, width=1530, height=660)

        Label(
            bg_label,
            text="STUDENT ATTENDANCE MANAGEMENT SYSTEM",
            font=("times new roman", 30, "bold"),
            bg="white",
            fg="green"
        ).place(x=0, y=0, width=1530, height=50)

        self.main_frame = Frame(bg_label, bd=2, bg="white")
        self.main_frame.place(x=10, y=55, width=1510, height=595)

    def _load_frames(self):
        left = LabelFrame(
            self.main_frame, text="Student Information",
            font=("times new roman", 12, "bold"),
            bg="white", bd=2, relief=RIDGE
        )
        left.place(x=10, y=10, width=740, height=570)

        img = Image.open(r"logos\image.png").resize((730, 130), Image.Resampling.LANCZOS)
        self.left_img = ImageTk.PhotoImage(img)
        Label(left, image=self.left_img).place(x=2, y=0, width=730, height=130)

        form = Frame(left, bg="white", bd=2, relief=RIDGE)
        form.place(x=5, y=135, width=725, height=330)

        self._create_entry(form, "Attendance ID", self.var_att_id, 0, 0)
        self._create_entry(form, "Roll", self.var_roll, 0, 2)
        self._create_entry(form, "Name", self.var_name, 1, 0)
        self._create_entry(form, "Department", self.var_dep, 1, 2)
        self._create_entry(form, "Time", self.var_time, 2, 0)
        self._create_entry(form, "Date", self.var_date, 2, 2)

        Label(form, text="Attendance Status", font=("times new roman", 12, "bold"), bg="white") \
            .grid(row=3, column=0, padx=10, pady=5, sticky=W)

        ttk.Combobox(
            form, textvariable=self.var_status,
            values=("Status", "Present", "Absent"),
            state="readonly", width=20
        ).grid(row=3, column=1, padx=10, pady=5)

        btn = Frame(left, bg="white", bd=2, relief=RIDGE)
        btn.place(x=5, y=470, width=725, height=60)

        self._create_button(btn, "Import CSV", self.importCsv, 0)
        self._create_button(btn, "Export CSV", self.exportCsv, 1)
        self._create_button(btn, "Update", self.update_data, 2)
        self._create_button(btn, "Reset", self.reset_data, 3)

    def _load_table(self):
        right = LabelFrame(
            self.main_frame, text="Attendance Database",
            font=("times new roman", 12, "bold"),
            bg="white", bd=2, relief=RIDGE
        )
        right.place(x=760, y=10, width=740, height=570)

        frame = Frame(right, bg="white", bd=2, relief=RIDGE)
        frame.place(x=5, y=10, width=725, height=530)

        scroll_x = ttk.Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(frame, orient=VERTICAL)

        self.table = ttk.Treeview(
            frame,
            columns=("id", "roll", "name", "dep", "time", "date", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        for col, txt in zip(
            ("id", "roll", "name", "dep", "time", "date", "status"),
            ("Attendance ID", "Roll", "Name", "Department", "Time", "Date", "Status")
        ):
            self.table.heading(col, text=txt)
            self.table.column(col, width=100)

        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<ButtonRelease-1>", self.get_cursor)

    # ================= HELPERS =================
    def _create_entry(self, parent, label, var, r, c):
        Label(parent, text=label, font=("times new roman", 12, "bold"), bg="white") \
            .grid(row=r, column=c, padx=10, pady=5, sticky=W)
        ttk.Entry(parent, textvariable=var, width=22) \
            .grid(row=r, column=c + 1, padx=10, pady=5)

    def _create_button(self, parent, text, cmd, col):
        Button(
            parent, text=text, command=cmd, width=17,
            font=("times new roman", 12, "bold"),
            bg="blue", fg="white"
        ).grid(row=0, column=col, padx=5, pady=10)

    def _set_current_datetime(self):
        now = datetime.now()
        self.var_date.set(now.strftime("%d-%m-%Y"))
        self.var_time.set(now.strftime("%H:%M:%S"))

    # ================= CSV FUNCTIONS =================
    def importCsv(self):
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file:
            return

        self.data.clear()
        try:
            with open(file, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row not in self.data:
                        self.data.append(row)
            self.fetchData()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportCsv(self):
        if not self.data:
            messagebox.showerror("No Data", "Nothing to export")
            return

        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if not file:
            return

        with open(file, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(self.data)

        messagebox.showinfo("Success", "Data exported successfully")

    def fetchData(self):
        self.table.delete(*self.table.get_children())
        for row in self.data:
            self.table.insert("", END, values=row)

    # ================= TABLE =================
    def get_cursor(self, _):
        row = self.table.item(self.table.focus()).get("values")
        if not row:
            return

        self.var_att_id.set(row[0])
        self.var_roll.set(row[1])
        self.var_name.set(row[2])
        self.var_dep.set(row[3])
        self.var_time.set(row[4])
        self.var_date.set(row[5])
        self.var_status.set(row[6])

    # ================= ACTIONS =================
    def reset_data(self):
        self.var_att_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_dep.set("")
        self.var_status.set("Status")
        self._set_current_datetime()

    def update_data(self):
        messagebox.showinfo("Update", "Connect this with database if required")


if __name__ == "__main__":
    root = Tk()
    Attendance(root)
    root.mainloop()
