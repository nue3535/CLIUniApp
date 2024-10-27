import random
import pickle
import re
import os

# Model Classes
class Subject:
    def __init__(self, name):
        self.id = f"{random.randint(1, 999):03d}"
        self.name = name
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()
    
    def calculate_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'F'

class Student:
    def __init__(self, name, email, password):
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def enroll_subject(self, subject_name):
        if len(self.subjects) < 4:
            new_subject = Subject(subject_name)
            self.subjects.append(new_subject)
            return f"Enrolled in {subject_name}"
        else:
            return "You cannot enroll in more than 4 subjects."

    def remove_subject(self, subject_id):
        self.subjects = [s for s in self.subjects if s.id != subject_id]

    def view_enrollments(self):
        return [(subject.id, subject.name, subject.mark, subject.grade) for subject in self.subjects]

    def change_password(self, new_password):
        self.password = new_password

class Database:
    FILE_NAME = 'students.data'

    @staticmethod
    def save_students(students):
        with open(Database.FILE_NAME, 'wb') as file:
            pickle.dump(students, file)

    @staticmethod
    def load_students():
        if os.path.exists(Database.FILE_NAME):
            with open(Database.FILE_NAME, 'rb') as file:
                return pickle.load(file)
        return {}

    @staticmethod
    def clear_data():
        if os.path.exists(Database.FILE_NAME):
            os.remove(Database.FILE_NAME)

# Controller Classes
class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def register_student(self, name, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            return "Invalid email or password format."
        if email in self.students:
            return "Student already registered."
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

# Main Application
def main():
    student_controller = StudentController()
    admin_controller = AdminController()

    while True:
        print("\nUniversity System:")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")
        choice = input("Select an option: ").strip().lower()

        if choice == 'a':
            handle_admin_menu(admin_controller)
        elif choice == 's':
            handle_student_menu(student_controller)
        elif choice == 'x':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, please try again.")

def handle_admin_menu(admin_controller):
    while True:
        print("\nAdmin Menu:")
        print("(S) Show all students")
        print("(R) Remove a student")
        print("(G) Group students by grade")
        print("(P) Partition students into PASS/FAIL categories")
        print("(C) Clear all data")
        print("(X) Exit")
        choice = input("Select an option: ").strip().lower()

        if choice == 's':
            students = admin_controller.view_all_students()
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")
        elif choice == 'r':
            email = input("Enter the email of the student to remove: ")
            result = admin_controller.remove_student(email)
            print(result)
        elif choice == 'g':
            groups = admin_controller.group_students()
            for grade, students in groups.items():
                print(f"\nGrade {grade}:")
                for student in students:
                    print(f"  - ID: {student.id}, Name: {student.name}")
        elif choice == 'p':
            partitions = admin_controller.partition_students()
            print("\nPass:")
            for student in partitions['Pass']:
                print(f"  - ID: {student.id}, Name: {student.name}")
            print("\nFail:")
            for student in partitions['Fail']:
                print(f"  - ID: {student.id}, Name: {student.name}")
        elif choice == 'c':
            print(admin_controller.clear_all_students())
        elif choice == 'x':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice, please try again.")

def handle_student_menu(student_controller):
    while True:
        print("\nStudent Menu:")
        print("(L) Login")
        print("(R) Register")
        print("(X) Exit")
        choice = input("Select an option: ").strip().lower()

        if choice == 'r':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            result = student_controller.register_student(name, email, password)
            print(result)
        elif choice == 'l':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            student = student_controller.login_student(email, password)
            if student:
                print("Login successful!")
                handle_subject_enrollment(student, student_controller)
            else:
                print("Invalid email or password.")
        elif choice == 'x':
            print("Exiting Student Menu.")
            break
        else:
            print("Invalid choice, please try again.")

def handle_subject_enrollment(student, student_controller):
    while True:
        print("\nSubject Enrollment System:")
        print("(C) Change password")
        print("(E) Enroll in a subject")
        print("(R) Remove a subject")
        print("(S) Show enrolled subjects")
        print("(X) Exit")
        choice = input("Select an option: ").strip().lower()

        if choice == 'c':
            new_password = input("Enter new password: ")
            student.change_password(new_password)
            student_controller.students[student.email] = student
            Database.save_students(student_controller.students)
            print("Password changed successfully.")
        elif choice == 'e':
            subject_name = input("Enter the subject name to enroll: ")
            result = student.enroll_subject(subject_name)
            student_controller.students[student.email] = student
            Database.save_students(student_controller.students)
            print(result)
        elif choice == 'r':
            subject_id = input("Enter the subject ID to remove: ")
            student.remove_subject(subject_id)
            student_controller.students[student.email] = student
            Database.save_students(student_controller.students)
            print(f"Subject with ID {subject_id} removed.")
        elif choice == 's':
            enrollments = student.view_enrollments()
            for enrollment in enrollments:
                print(f"ID: {enrollment[0]}, Name: {enrollment[1]}, Mark: {enrollment[2]}, Grade: {enrollment[3]}")
        elif choice == 'x':
            print("Exiting Subject Enrollment System.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
