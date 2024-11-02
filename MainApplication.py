# MainApplication.py

from Controller import StudentController, AdminController
from Model import Database
import random
from Model import Student
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    student_controller = StudentController()
    admin_controller = AdminController()

    while True:
        choice = input(f"{Fore.CYAN}University System: (A)dmin, (S)tudent, or X: {Style.RESET_ALL}")
        
        if choice == 'A':
            handle_admin_menu(admin_controller)
        elif choice == 'S':
            handle_student_menu(student_controller)
        elif choice == 'X':
            print(f"{Fore.YELLOW}Thank You")
            break
        else:
            print(f"{Fore.RED}Invalid Input")

def handle_admin_menu(admin_controller):
    
    while True:
        choice = input(f"{Fore.CYAN}        Admin System (c/g/p/r/s/x): {Style.RESET_ALL}")
        if choice == 's':
            students = admin_controller.view_all_students()
            print(f"{Fore.YELLOW}        Student List")
            if not students:
                print("        <Nothing to Display>")
            else:
                for student in students:
                    print(f"        {student[1]} :: {student[0]} --> Email: {student[2]}")
        elif choice == 'r':
            student_id = input("        Remove by ID: ")
            admin_controller.remove_student(student_id)
        elif choice == 'g':
            groups = admin_controller.group_students()
            print(f"{Fore.YELLOW}        Grade Grouping")
            if all(not students for students in groups.values()):
                print("        <Nothing to Display>")
            else:
                for grade, students in groups.items():
                     if students:  # 檢查該分組是否有學生
                        student_descriptions = [
                            f"{student.name} :: {student.id} --> GRADE: {grade} - MARK: {admin_controller.calculate_average(student):.2f}"
                            for student in students
                        ]
                        print(f"        {grade} --> [{' , '.join(student_descriptions)}]")
        elif choice == 'p':
            partitions = admin_controller.partition_students()
            print(f"{Fore.YELLOW}        PASS/FAIL Partition")
            pass_list = [
                f"{student.name} :: {student.id} --> GRADE: {student.subjects[0].grade} - MARK: {admin_controller.calculate_average(student):.2f}"
                for student in partitions['Pass']
            ]   
            fail_list = [
                f"{student.name} :: {student.id} --> GRADE: {student.subjects[0].grade} - MARK: {admin_controller.calculate_average(student):.2f}"
                for student in partitions['Fail']
            ]
            print("        PASS -->", pass_list)
            print("        FAIL -->", fail_list)
        elif choice == 'c':
            print(f"{Fore.YELLOW}        Clearing students database")
            while True:
                clear_data = input(f"{Fore.RED}        Are you sure you want to clear the database (Y)ES/(N)O: {Style.RESET_ALL}")
                if clear_data == "Y":
                    print(admin_controller.clear_all_students())
                    break
                elif clear_data == "N":
                    break
                else:
                    print(f"{Fore.RED}        Invalid Input")               
        elif choice == 'x':
            break
        else:
            print(f"{Fore.RED}        Invalid choice, please try again.")

def handle_student_menu(student_controller):
   while True:
        choice = input(f"{Fore.CYAN}        Student System (l/r/x): {Style.RESET_ALL}")

        if choice == 'r':
            print(f"{Fore.GREEN}        Student Sign Up")
            while True:
                email = input("        Email: ")
                if not email:
                    print(f"{Fore.RED}        Please enter your given email.")
                    continue
                password = input("        Password: ")
                if not password:
                    print(f"{Fore.RED}        Please enter your given password.")
                    continue
                result = student_controller.register_student(email, password)
                if result == "Student already registered.":
                    break
                elif result == "Registration successful.":
                      break  
        elif choice == 'l':
            print(f"{Fore.GREEN}        Student Sign In")
            while True:
                email = input("        Email: ")
                if not email:
                    print(f"{Fore.RED}        Please enter your given email.")
                    continue
                password = input("        Password: ")
                if not password:
                    print(f"{Fore.RED}        Please enter your given password.")
                    continue
                result = student_controller.login_student(email, password)
                if result == "Incorrect email or password format":
                    continue
                if isinstance(result, Student) :
                    handle_subject_enrollment(result, student_controller)
                    break
                elif result == "Student does not exist":
                    break
        elif choice == 'x':
            break
        else:
            print(f"{Fore.RED}        Invalid choice, please try again.")

def handle_subject_enrollment(student, student_controller):
    while True:
        choice = input(f"{Fore.CYAN}                Student Course Menu (c/e/r/s/x): {Style.RESET_ALL}")
        
        if choice == 'c':
            print(f"{Fore.YELLOW}                Updating Password")
            while True:
                new_password = input("                New password: ")
                if StudentController.is_valid_password(new_password):
                    while True:
                        confirm_new_password = input("                Confirm password: ")
                        if new_password == confirm_new_password:
                            student.change_password(new_password)
                            student_controller.students[student.email] = student
                            Database.save_students(student_controller.students)
                            break
                        else:
                            print(f"{Fore.RED}                Password does not match - try again")
                            continue
                else:
                    print(f"{Fore.RED}                Incorrect password format")
                    continue
                break
        elif choice == 'e':
            enrollments = student.view_enrollments()
            if len(enrollments) == 4:
                print(f"{Fore.RED}                Students are allowed to enrol in 4 subjects only")
            else:
                subject_id = f"{random.randint(1, 999):03d}"
                result = student.enroll_subject(subject_id)
                student_controller.students[student.email] = student
                Database.save_students(student_controller.students)
                print(result)
                enrollments = student.view_enrollments()
                print(f"{Fore.YELLOW}                You are now enrolled in " + str(len(enrollments)) + " out of 4 subjects")
        elif choice == 'r':
            subject_id = input("                Remove subject by ID: ")
            student.remove_subject(subject_id)
            student_controller.students[student.email] = student
            Database.save_students(student_controller.students)
            print(f"{Fore.YELLOW}                Droping Subject-{subject_id}")
            enrollments = student.view_enrollments()
            print(f"{Fore.YELLOW}                You are now enrolled " + str(len(enrollments)) + " out of 4 subjects")
        elif choice == 's':
            enrollments = student.view_enrollments()
            print(f"{Fore.YELLOW}                Showing " + str(len(enrollments)) + " subjects")
            for enrollment in enrollments:
                print(f"                [ Subject::{enrollment[0]} -- mark = {enrollment[1]} -- grade = {enrollment[2]} ]")
        elif choice == 'x':
            break
        else:
            print(f"{Fore.RED}                Invalid choice, please try again.")

if __name__ == "__main__":
    main()