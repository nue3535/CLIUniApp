def main():
    student_controller = StudentController()
    admin_controller = AdminController()

    while True:
        print("University System:")
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
    print("Admin Menu:")
    # Implement admin functionalities based on the specification
    # Example: admin_controller.remove_student(email)

def handle_student_menu(student_controller):
    print("Student Menu:")
    # Implement student functionalities based on the specification
    # Example: student_controller.register_student(name, email, password)

if __name__ == "__main__":
    main()
