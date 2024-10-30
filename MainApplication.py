# MainApplication.py

from Controller import StudentController, AdminController
from Model import Database
import random

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
            print("Student List")
            for student in students:
                print(f"{student[1]} :: {student[0]} --> Email: {student[2]}")
        elif choice == 'r':
           
            student_id = input("Remove by ID: ")
            admin_controller.remove_student(student_id)
           
        elif choice == 'g':
            groups = admin_controller.group_students()
            print("Grade Grouping")
            for grade, students in groups.items():
                if students:  # 檢查該分組是否有學生
                    student_descriptions = [
                        f"{student.name} :: {student.id} --> GRADE: {grade} - MARK: {admin_controller.calculate_average(student):.2f}"
                        for student in students
                    ]
                    print(f"{grade} --> [{' , '.join(student_descriptions)}]")
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
        print("(R) Register")
        print("(L) Login")
        print("(X) Exit")
        choice = input("Select an option: ").strip().lower()

        if choice == 'r':
            print("Student Sign Up")
            while True:
                email = input("Enter your email: ")
                if not email:
                    print("Please enter your given email.")
                    continue
                password = input("Enter your password: ")
                if not password:
                    print("Please enter your given password.")
                    continue
                result = student_controller.register_student_cli(email, password)
                print(result)
                if result == "Registration successful.":
                    break
                
        elif choice == 'l':
            print("Student Sign In")
            while True:
                email = input("Enter your email: ")
                if not email:
                    print("Please enter your given email.")
                    continue
                password = input("Enter your password: ")
                if not password:
                    print("Please enter your given password.")
                    continue
                student = student_controller.login_student(email, password)
                if student:
                    print("Login successful!")
                    handle_subject_enrollment(student, student_controller)
                    break
                else:
                    print("Invalid email or password.")
                    continue
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
            print("Updating Password")
            while True:
                new_password = input("Enter new password: ")
                if StudentController.is_valid_password(new_password):
                    while True:
                        confirm_new_password = input("Confirm new password: ")
                        if new_password == confirm_new_password:
                            student.change_password(new_password)
                            student_controller.students[student.email] = student
                            Database.save_students(student_controller.students)
                            print("Password changed successfully.")
                            break
                        else:
                            print("Password does not match - try again")
                            continue
                else:
                    print("Password does not valid - try again")
                    continue
                break
        elif choice == 'e':
            # subject_name = input("Enter the subject name to enroll: ")
            enrollments = student.view_enrollments()
            if len(enrollments) == 4:
                print("Students are allowed to enroll in 4 subjects only")
            else:
                subject_id = f"{random.randint(1, 999):03d}"
                result = student.enroll_subject(subject_id)
                student_controller.students[student.email] = student
                Database.save_students(student_controller.students)
                print(result)
                enrollments = student.view_enrollments()
                print("You are now enrolled " + str(len(enrollments)) + " out of 4 subjects")
        elif choice == 'r':
            subject_id = input("Enter the subject ID to remove: ")
            student.remove_subject(subject_id)
            student_controller.students[student.email] = student
            Database.save_students(student_controller.students)
            print(f"Droping Subject-{subject_id}")
            enrollments = student.view_enrollments()
            print("You are now enrolled " + str(len(enrollments)) + " out of 4 subjects")
        elif choice == 's':
            enrollments = student.view_enrollments()
            print("Showing " + str(len(enrollments)) + " subjects")
            for enrollment in enrollments:
                print(f"ID: {enrollment[0]}, Mark: {enrollment[1]}, Grade: {enrollment[2]}")
        elif choice == 'x':
            print("Exiting Subject Enrollment System.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()