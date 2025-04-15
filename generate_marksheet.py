import sqlite3
from fpdf import FPDF

def create_marksheet(roll_no):
    conn = sqlite3.connect("ResultManagementSystem.db")
    cur = conn.cursor()

    # Fetch student details
    cur.execute('SELECT name, course FROM result WHERE roll=?', (roll_no,))
    student = cur.fetchone()

    if not student:
        print("Student not found!")
        return

    name, course = student

    # Fetch marks details
    cur.execute('SELECT marks_obtain, full_marks, percentage FROM result WHERE roll=?', (roll_no,))
    marks_data = cur.fetchone()

    if not marks_data:
        print("Marks data not found!")
        return

    marks_obtained, full_marks, percentage = marks_data

    # Generate PDF Marksheet
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Student Marksheet", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Roll No: {roll_no}", ln=True)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Course: {course}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Marks Details", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Marks Obtained: {marks_obtained} / {full_marks}", ln=True)
    pdf.cell(200, 10, f"Percentage: {percentage}%", ln=True)

    # Save PDF
    pdf.output(f"marksheet_{roll_no}.pdf")
    conn.close()

    print(f"Marksheet generated for {name} (Roll No: {roll_no})")

# Example usage
roll_number = input("Enter Roll Number: ")
create_marksheet(roll_number)
