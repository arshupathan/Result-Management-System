from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk 
from course import CourseClass
from student import StudentClass
from result import ResultClass
from ViewResult import ViewClass
import sqlite3 
import os
import time
import math

class ResultManagementSystem:
    def __init__(self, home):
        self.home = home
        self.home.title("Student Result Management System")
        self.home.geometry("1450x700+0+0")
        self.home.config(bg="white")

        # Importing image logo (icons)
        self.logo = Image.open("images/logo.jpg")
        self.logo = self.logo.resize((90, 35), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)

        # Title of project
        title = Label(self.home, text="Student Result Management", padx=10, compound=LEFT, image=self.logo, font=("times new roman", 20, "bold"), bg="Dark Blue", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Menu 
        Frame1 = LabelFrame(self.home, text="Menu", font=("times new roman", 15, "bold"), bg="white")
        Frame1.place(x=10, y=70, width=1340, height=80)

        # SubMenu
        Button(Frame1, text="Course", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.add_course).place(x=20, y=5, width=200, height=40)
        Button(Frame1, text="Student", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.add_student).place(x=240, y=5, width=200, height=40)
        Button(Frame1, text="Result", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.add_result).place(x=460, y=5, width=200, height=40)
        Button(Frame1, text="View Student Result", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.add_view).place(x=680, y=5, width=200, height=40)
        Button(Frame1, text="Logout", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.logout).place(x=900, y=5, width=200, height=40)
        Button(Frame1, text="Exit", font=("times new roman", 15, "bold"), bg="dark blue", fg="white", cursor="hand2", command=self.exit_app).place(x=1120, y=5, width=200, height=40)

        # Background Image
        self.bgImage = Image.open("Images/7.png")
        self.bgImage = self.bgImage.resize((900, 350), Image.Resampling.LANCZOS)
        self.bgImage = ImageTk.PhotoImage(self.bgImage)
        Label(self.home, image=self.bgImage).place(x=400, y=180, width=940, height=350)

        # Analog Clock
        self.clock_canvas = Canvas(self.home, width=200, height=200, bg="white", highlightthickness=0)
        self.clock_canvas.place(x=150, y=250)
        self.update_clock()

        # Update Details
        self.totalCourse = Label(self.home, text="Total Courses \n 0 ", font=("times new roman", 20), bd=10, relief=RIDGE, bg="purple", fg="white")
        self.totalCourse.place(x=400, y=530, width=300, height=80)
        self.totalstudent = Label(self.home, text="Total Student \n 0 ", font=("times new roman", 20), bd=10, relief=RIDGE, bg="orange", fg="white")
        self.totalstudent.place(x=720, y=530, width=300, height=80)
        self.totalresults = Label(self.home, text="Total Results \n 0 ", font=("times new roman", 20), bd=10, relief=RIDGE, bg="coral", fg="white")
        self.totalresults.place(x=1040, y=530, width=300, height=80)

        # Footer
        Label(self.home, text="Contact Me: \n  arshiya@gmail.com", font=("times new roman", 13, "bold"), bg="grey", fg="white").pack(side=BOTTOM, fill=X)

        self.update_details()

    # Logout Function
    def logout(self):
        self.home.destroy()
        os.system("python main.py")  # Redirect to the login page if applicable

    # Exit Function
    def exit_app(self):
        self.home.quit()

    # Clock Update Function
    def update_clock(self):
        self.clock_canvas.delete("all")
        self.clock_canvas.create_oval(10, 10, 190, 190, outline="black", width=3)
        
        time_now = time.localtime()
        sec = time_now.tm_sec
        min = time_now.tm_min
        hour = time_now.tm_hour % 12
        
        self.draw_hand(90, 90, 70, (hour * 30 + min * 0.5), "black", 6)  # Hour hand
        self.draw_hand(90, 90, 85, (min * 6), "blue", 4)  # Minute hand
        self.draw_hand(90, 90, 90, (sec * 6), "red", 2)  # Second hand
        
        self.clock_canvas.after(1000, self.update_clock)

    def draw_hand(self, x, y, length, angle, color, width):
        radian = math.radians(angle - 90)
        x_end = x + length * math.cos(radian)
        y_end = y + length * math.sin(radian)
        self.clock_canvas.create_line(x, y, x_end, y_end, fill=color, width=width)

    # Update Details Function
    def update_details(self):
        conn = sqlite3.connect(database="ResultManagementSystem.db")
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM course")
            self.totalCourse.config(text=f"Total Course\n[{len(cur.fetchall())}]")
            cur.execute("SELECT * FROM student")
            self.totalstudent.config(text=f"Total Students\n[{len(cur.fetchall())}]")
            cur.execute("SELECT * FROM result")
            self.totalresults.config(text=f"Total Results\n[{len(cur.fetchall())}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # Submenu Functions
    def add_course(self):
        CourseClass(Toplevel(self.home))
    
    def add_student(self):
        StudentClass(Toplevel(self.home))
    
    def add_result(self):
        ResultClass(Toplevel(self.home))
    
    def add_view(self):
        ViewClass(Toplevel(self.home))

if __name__ == "__main__":
    home = Tk()
    ResultManagementSystem(home)
    home.mainloop()
