# FrontendApp.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from Controller import StudentController, AdminController
from Model import Database

class CLIUniAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CLIUniApp - University System")

        self.student_controller = StudentController()
        self.admin_controller = AdminController()

        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="University System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Admin", command=self.admin_menu, width=20).pack(pady=5)
        tk.Button(self.root, text="Student", command=self.student_menu, width=20).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=5)

    def admin_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Menu", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Show all students", command=self.show_all_students, width=30).pack(pady=5)
        tk.Button(self.root, text="Remove a student", command=self.remove_student, width=30).pack(pady=5)
        tk.Button(self.root, text="Group students by grade", command=self.group_students, width=30).pack(pady=5)
        tk.Button(self.root, text="Partition students (Pass/Fail)", command=self.partition_students, width=30).pack(pady=5)
        tk.Button(self.root, text="Clear all data", command=self.clear_data, width=30).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=30).pack(pady=5)

    def student_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Student Menu", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_student, width=30).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login_student, width=30).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=30).pack(pady=5)

    def show_all_students(self):
        students = self.admin_controller.view_all_students()
        if students:
            info = "\n".join([f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}" for student in students])
        else:
            info = "No students found."
        messagebox.showinfo("All Students", info)

    def remove_student(self):
        email = simpledialog.askstring("Remove Student", "Enter student email:")
        if email:
            result = self.admin_controller.remove_student(email)
            messagebox.showinfo("Remove Student", result)

    def group_students(self):
        groups = self.admin_controller.group_students()
        info = ""
        for grade, students in groups.items():
            info += f"\nGrade {grade}:\n"
            for student in students:
                info += f"  - ID: {student.id}, Name: {student.name}\n"
        messagebox.showinfo("Group Students by Grade", info)

    def partition_students(self):
        partitions = self.admin_controller.partition_students()
        info = "\nPass:\n"
        for student in partitions['Pass']:
            info += f"  - ID: {student.id}, Name: {student.name}\n"
        info += "\nFail:\n"
        for student in partitions['Fail']:
            info += f"  - ID: {student.id}, Name: {student.name}\n"
        messagebox.showinfo("Partition Students (Pass/Fail)", info)

    def clear_data(self):
        result = self.admin_controller.clear_all_students()
        messagebox.showinfo("Clear Data", result)

    def register_student(self):
        email = simpledialog.askstring("Register", "Enter your email:")
        if not email:
            return
        password = simpledialog.askstring("Register", "Enter your password:")
        if not password:
            return
        if email and password:
            result = self.student_controller.register_student(email, password)
            messagebox.showinfo("Register", result)

    def login_student(self):
        email = simpledialog.askstring("Login", "Enter your email:")
        if not email:
            return
        password = simpledialog.askstring("Login", "Enter your password:")
        if not password:
            return
        if email and password:
            student = self.student_controller.login_student(email, password)
            if student:
                self.subject_enrollment_menu(student)
            else:
                messagebox.showerror("Login", "Invalid email or password.")

    def subject_enrollment_menu(self, student):
        self.clear_window()
        tk.Label(self.root, text="Subject Enrollment System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Change Password", command=lambda: self.change_password(student), width=30).pack(pady=5)
        tk.Button(self.root, text="Enroll in a subject", command=lambda: self.enroll_subject(student), width=30).pack(pady=5)
        tk.Button(self.root, text="Remove a subject", command=lambda: self.remove_subject(student), width=30).pack(pady=5)
        tk.Button(self.root, text="Show enrolled subjects", command=lambda: self.show_enrolled_subjects(student), width=30).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=30).pack(pady=5)

    def change_password(self, student):
        new_password = simpledialog.askstring("Change Password", "Enter new password:")
        if new_password:
            student.change_password(new_password)
            self.student_controller.students[student.email] = student
            Database.save_students(self.student_controller.students)
            messagebox.showinfo("Change Password", "Password changed successfully.")

    def enroll_subject(self, student):
        subject_name = simpledialog.askstring("Enroll Subject", "Enter the subject name:")
        if subject_name:
            result = student.enroll_subject(subject_name)
            self.student_controller.students[student.email] = student
            Database.save_students(self.student_controller.students)
            messagebox.showinfo("Enroll Subject", result)

    def remove_subject(self, student):
        subject_id = simpledialog.askstring("Remove Subject", "Enter the subject ID:")
        if subject_id:
            student.remove_subject(subject_id)
            self.student_controller.students[student.email] = student
            Database.save_students(self.student_controller.students)
            messagebox.showinfo("Remove Subject", f"Subject with ID {subject_id} removed.")

    def show_enrolled_subjects(self, student):
        enrollments = student.view_enrollments()
        if enrollments:
            info = "\n".join([f"ID: {enrollment[0]}, Name: {enrollment[1]}, Mark: {enrollment[2]}, Grade: {enrollment[3]}" for enrollment in enrollments])
        else:
            info = "No subjects enrolled."
        messagebox.showinfo("Enrolled Subjects", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = CLIUniAppGUI(root)
    root.mainloop()
