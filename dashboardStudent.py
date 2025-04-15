from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import os
from fpdf import FPDF

class studentSystem:
    def __init__(self, home):
        self.home = home
        self.home.title("Student Page")
        self.home.geometry("1450x700+0+0")
        self.home.config(bg="white")

        # Title of Student Page
        title = Label(self.home, text="Student Result", font=("times new roman", 20, "bold"), bg="purple", fg="white").place(x=0, y=0, relwidth=1, height=50)

        # Searching Section
        self.var_search = StringVar()
        lbl_rollno = Label(self.home, text="Enter Roll No. ", font=("times new roman", 30, "bold"), bg="white").place(x=450, y=60)
        txt_rollno1 = Entry(self.home, textvariable=self.var_search, font=("times new roman", 15, "bold"), bg="lightyellow").place(x=700, y=70, width=180, height=35)
        btn_search = Button(self.home, text="Search", font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2", command=self.search).place(x=900, y=70, width=100, height=35)
        btn_clear = Button(self.home, text="Clear", font=("times new roman", 15, "bold"), bg="orange", fg="white", cursor="hand2", command=self.clear).place(x=1020, y=70, width=100, height=35)
        button_Logout = Button(self.home, text="Logout", font=("times new roman", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.logout).place(x=1170, y=70, width=100, height=35)

        # Result Display Labels
        fields = ["Roll No.", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage"]
        positions = [100, 290, 480, 670, 860, 1050]
        self.result_labels = {}

        for i, field in enumerate(fields):
            Label(self.home, text=field, font=("times new roman", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=positions[i], y=200, width=190, height=90)
            self.result_labels[field] = Label(self.home, font=("times new roman", 15, "bold"), bg="white", bd=2, relief=GROOVE)
            self.result_labels[field].place(x=positions[i], y=290, width=190, height=90)

    # Search Functionality
    def search(self):
        conn = sqlite3.connect("ResultManagementSystem.db")
        cur = conn.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.home)
            else:
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row:
                    self.var_id = row[0]
                    self.result_labels["Roll No."].config(text=row[1])
                    self.result_labels["Name"].config(text=row[2])
                    self.result_labels["Course"].config(text=row[3])
                    self.result_labels["Marks Obtained"].config(text=row[4])
                    self.result_labels["Total Marks"].config(text=row[5])
                    self.result_labels["Percentage"].config(text=row[6])
                else:
                    messagebox.showerror("Error", "No record found", parent=self.home)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.home)
        finally:
            conn.close()

    # Clear Fields
    def clear(self):
        self.var_id = ""
        for label in self.result_labels.values():
            label.config(text="")
        self.var_search.set("")

    # Logout Function
    def logout(self):
        op = messagebox.askyesno("Confirm Again", "Do You really Want to Logout?", parent=self.home)
        if op:
            self.home.destroy()
            os.system("Python Login.py")

    # Generate Marksheet Functionality
    def generate_marksheet(self):
        roll_no = self.var_search.get()
        if roll_no == "":
            messagebox.showerror("Error", "Please enter a Roll No. to generate the marksheet", parent=self.home)
            return

        conn = sqlite3.connect("ResultManagementSystem.db")
        cur = conn.cursor()

        # Fetch Student Details
        cur.execute("SELECT name, course, dob, contact FROM student WHERE roll=?", (roll_no,))
        student = cur.fetchone()

        if not student:
            messagebox.showerror("Error", "Student record not found!", parent=self.home)
            conn.close()
            return

        name, course, dob, contact = student

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Student Marksheet", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Roll No: {roll_no}", ln=True)
        pdf.cell(200, 10, f"Name: {name}", ln=True)
        pdf.cell(200, 10, f"Course: {course}", ln=True)
        pdf.cell(200, 10, f"D.O.B: {dob}", ln=True)
        pdf.cell(200, 10, f"Contact: {contact}", ln=True)

        # Fetch Marks
        cur.execute("SELECT subject, marks FROM marks WHERE roll=?", (roll_no,))
        marks = cur.fetchall()

        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Marks Obtained", ln=True)

        pdf.set_font("Arial", size=12)
        for subject, mark in marks:
            pdf.cell(200, 10, f"{subject}: {mark}", ln=True)

        filename = f"marksheet_{roll_no}.pdf"
        pdf.output(filename)
        conn.close()

        messagebox.showinfo("Success", f"Marksheet generated successfully!\nFile: {filename}", parent=self.home)


if __name__ == "__main__":
    home = Tk()
    obj = studentSystem(home)
    home.mainloop() 