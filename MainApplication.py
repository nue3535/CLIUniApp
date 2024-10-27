# MainApplication.py

from Controller import StudentController, AdminController
from Model import Database

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
