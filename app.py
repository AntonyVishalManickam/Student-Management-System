import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- DATABASE SETUP ---
def setup_db():
    conn = sqlite3.connect("college_gui.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            marks REAL,
            attendance REAL
        )
    ''')
    conn.commit()
    conn.close()

# --- GUI APPLICATION CLASS ---
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x500")
        self.root.configure(bg="#f4f4f4")

        setup_db()

        # --- TITLE ---
        title = tk.Label(self.root, text="Student Management System", font=("Arial", 20, "bold"), bg="#004080", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)

        # --- LEFT FRAME: DATA ENTRY (CRUD Forms) ---
        entry_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        entry_frame.place(x=20, y=60, width=350, height=420)

        tk.Label(entry_frame, text="Manage Records", font=("Arial", 15, "bold"), bg="white").grid(row=0, columnspan=2, pady=10)

        # Input Fields
        tk.Label(entry_frame, text="Roll Number:", bg="white", font=("Arial", 11)).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.roll_var = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.roll_var, font=("Arial", 11), bd=1, relief=tk.SOLID).grid(row=1, column=1, pady=10, padx=10)

        tk.Label(entry_frame, text="Student Name:", bg="white", font=("Arial", 11)).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.name_var, font=("Arial", 11), bd=1, relief=tk.SOLID).grid(row=2, column=1, pady=10, padx=10)

        tk.Label(entry_frame, text="Course:", bg="white", font=("Arial", 11)).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.course_var = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.course_var, font=("Arial", 11), bd=1, relief=tk.SOLID).grid(row=3, column=1, pady=10, padx=10)

        tk.Label(entry_frame, text="Marks (0-100):", bg="white", font=("Arial", 11)).grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.marks_var = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.marks_var, font=("Arial", 11), bd=1, relief=tk.SOLID).grid(row=4, column=1, pady=10, padx=10)

        tk.Label(entry_frame, text="Attendance %:", bg="white", font=("Arial", 11)).grid(row=5, column=0, pady=10, padx=10, sticky="w")
        self.attendance_var = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.attendance_var, font=("Arial", 11), bd=1, relief=tk.SOLID).grid(row=5, column=1, pady=10, padx=10)

        # Buttons
        btn_frame = tk.Frame(entry_frame, bg="white")
        btn_frame.grid(row=6, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Add", width=8, bg="#28a745", fg="white", command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=8, bg="#ffc107", command=self.update_student).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=8, bg="#dc3545", fg="white", command=self.delete_student).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", width=8, bg="#6c757d", fg="white", command=self.clear_fields).grid(row=0, column=3, padx=5)

        # --- RIGHT FRAME: DATA TABLE (Viewing Records) ---
        table_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        table_frame.place(x=390, y=60, width=590, height=420)

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.student_table = ttk.Treeview(table_frame, columns=("roll", "name", "course", "marks", "attendance"), yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("marks", text="Marks")
        self.student_table.heading("attendance", text="Attendance %")

        self.student_table['show'] = 'headings'
        self.student_table.column("roll", width=100)
        self.student_table.column("name", width=150)
        self.student_table.column("course", width=150)
        self.student_table.column("marks", width=80)
        self.student_table.column("attendance", width=90)

        self.student_table.pack(fill=tk.BOTH, expand=1)
        
        # Bind clicking a row to fill the entry fields
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # --- CRUD FUNCTIONS ---
    def add_student(self):
        if self.roll_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("Error", "Roll Number and Name are required!")
            return
        try:
            conn = sqlite3.connect("college_gui.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (roll_no, name, course, marks, attendance) VALUES (?, ?, ?, ?, ?)",
                           (self.roll_var.get(), self.name_var.get(), self.course_var.get(), self.marks_var.get(), self.attendance_var.get()))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Student Added Successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll Number already exists!")

    def fetch_data(self):
        conn = sqlite3.connect("college_gui.db")
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name, course, marks, attendance FROM students")
        rows = cursor.fetchall()
        
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert('', tk.END, values=row)
        conn.close()

    def clear_fields(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.marks_var.set("")
        self.attendance_var.set("")

    def get_cursor(self, event):
        """Fills the entry fields when you click a row in the table."""
        cursor_row = self.student_table.focus()
        contents = self.student_table.item(cursor_row)
        row = contents['values']
        if row:
            self.roll_var.set(row[0])
            self.name_var.set(row[1])
            self.course_var.set(row[2])
            self.marks_var.set(row[3])
            self.attendance_var.set(row[4])

    def update_student(self):
        if self.roll_var.get() == "":
            messagebox.showerror("Error", "Select a student to update.")
            return
        conn = sqlite3.connect("college_gui.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=?, course=?, marks=?, attendance=? WHERE roll_no=?",
                       (self.name_var.get(), self.course_var.get(), self.marks_var.get(), self.attendance_var.get(), self.roll_var.get()))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Student Record Updated")

    def delete_student(self):
        if self.roll_var.get() == "":
            messagebox.showerror("Error", "Select a student to delete.")
            return
        conn = sqlite3.connect("college_gui.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll_no=?", (self.roll_var.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_fields()
        messagebox.showinfo("Success", "Student Deleted")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()