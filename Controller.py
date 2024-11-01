# Controller.py

import re
from Model import Student, Database
from tkinter import simpledialog

class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def register_student_cli(self, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            return "Invalid email or password format."
        print ("email and password formats acceptable")
        if email in Database.load_students():
            return "Student already registered."
        name = input("Enter your name: ")
        if not name:
            return "Please enter your given name."
        new_student = Student(name, email, password)
        self.students[email] = new_student
        Database.save_students(self.students)
        return "Registration successful."

    def register_student_gui(self, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            return "Invalid email or password format."
        print ("email and password formats acceptable")
        if email in self.students:
            # TODO: fix students.data methods so modify student's name here
            return "Student already registered."
        name = simpledialog.askstring("Register", "Enter your name:")
        if not name:
            return "Please enter your given name."
        new_student = Student(name, email, password)
        self.students[email] = new_student
        Database.save_students(self.students)
        return "Registration successfulddds."

    def login_student(self, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            return "Invalid email or password format."
        student = self.students.get(email)
        if student and student.password == password:
            return student
        return None

    @staticmethod
    def is_valid_email(email):
        return re.match(r"^[a-z]+\.[a-z]+@university\.com$", email)

    @staticmethod
    def is_valid_password(password):
        return re.match(r"^[A-Z][a-zA-Z]{4,}\d{3,}$", password)

class AdminController:
    def __init__(self):
        self.students = Database.load_students()

    def remove_student(self, student_id):
        self.students = {email: s for email, s in self.students.items() if s.id != student_id}
        Database.save_students(self.students)
        print(f"Removed student {student_id}")

    def partition_students(self):
        pass_students = [s for s in self.students.values() if self.calculate_average(s) >= 50]
        fail_students = [s for s in self.students.values() if self.calculate_average(s) < 50]
        return {"Pass": pass_students, "Fail": fail_students}

    def group_students(self):
        grade_groups = {'HD': [], 'D': [], 'C': [], 'P': [], 'F': []}
        for student in self.students.values():
            if student.subjects:  
                average_grade = student.subjects[0].grade  
                grade_groups[average_grade].append(student)
            
    
        return grade_groups

    def calculate_average(self, student):
        if not student.subjects:
            return 0
        return sum(subject.mark for subject in student.subjects) / len(student.subjects)

    def view_all_students(self):
        self.students = Database.load_students()
        return [(s.id, s.name, s.email) for s in self.students.values()]

    def clear_all_students(self):
        Database.clear_data()
        self.students = {}
        return "Student data cleared."