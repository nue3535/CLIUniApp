# Controller.py

import re
from Model import Student, Database
from tkinter import simpledialog

class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def register_student(self, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            return "Invalid email or password format."
        if email in self.students:
            return "Student already registered."
        name = simpledialog.askstring("Register", "Enter your name:")
        new_student = Student(name, email, password)
        self.students[email] = new_student
        Database.save_students(self.students)
        return "Registration successful."

    def login_student(self, email, password):
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

    def remove_student(self, email):
        if email in self.students:
            del self.students[email]
            Database.save_students(self.students)
            return "Student removed."
        return "Student not found."

    def partition_students(self):
        pass_students = [s for s in self.students.values() if self.calculate_average(s) >= 50]
        fail_students = [s for s in self.students.values() if self.calculate_average(s) < 50]
        return {"Pass": pass_students, "Fail": fail_students}

    def group_students(self):
        grouped = {}
        for student in self.students.values():
            for subject in student.subjects:
                grouped.setdefault(subject.grade, []).append(student)
        return grouped

    def calculate_average(self, student):
        if len(student.subjects) == 0:
            return 0
        return sum(subject.mark for subject in student.subjects) / len(student.subjects)

    def view_all_students(self):
        return [(s.id, s.name, s.email) for s in self.students.values()]

    def clear_all_students(self):
        Database.clear_data()
        self.students = {}
        return "All student data cleared."
