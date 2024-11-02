import tkinter as tk
from tkinter import messagebox
import random
from Controller import StudentController
from Model import Database, Student


class GUIUniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - GUIUniApp")
        self.root.geometry("400x300")
        self.student_controller = StudentController()
        self.current_student = None
        self.create_login_window()

    def create_login_window(self):
        self.clear_widget()
        
        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login_student).pack(pady=10)

    def login_student(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return
        result = self.student_controller.login_student(email, password)
        if isinstance(result, Student):
            self.current_student = result
            self.create_enrollment_window()
        elif result == "Incorrect email or password format":
            messagebox.showerror("Error", "Invalid email or password format.")
        elif result == "Student does not exist":
            messagebox.showerror("Error", "Student does not exist.")
        else:
            messagebox.showerror("Error", "Login failed. Please check your credentials.")

    def create_enrollment_window(self):
        self.clear_widget()

        self.root.title("Enrollment - GUIUniApp")

        tk.Label(self.root, text=f"Welcome, {self.current_student.name}").pack(pady=10)
        self.enroll_button = tk.Button(self.root, text="Enroll", command=self.enroll_subject)
        self.enroll_button.pack(pady=5)

        tk.Button(self.root, text="View Enrollments", command=self.view_enrollments).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.create_login_window).pack(pady=10)

    def enroll_subject(self):
        if len(self.current_student.subjects) >= 4:
            messagebox.showerror("Error", "You can enroll in up to 4 subjects only.")
            return

        subject_id = f"{random.randint(1, 999):03d}"  
        result = self.current_student.enroll_subject(subject_id)
        
        self.student_controller.students[self.current_student.email] = self.current_student
        Database.save_students(self.student_controller.students)

        messagebox.showinfo("Enrollment Success", result)

    def view_enrollments(self):
        self.clear_widget()
        
        self.root.title("Subject - GUIUniApp")
        tk.Label(self.root, text="Your Enrolled Subjects:").pack(pady=10)
        
        enrollments = self.current_student.view_enrollments()
        for subject in enrollments:
            tk.Label(self.root, text=f"Subject ID: {subject[0]}, Mark: {subject[1]}, Grade: {subject[2]}").pack(pady=2)
        
        tk.Button(self.root, text="Back", command=self.create_enrollment_window).pack(pady=10)

    def clear_widget(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
