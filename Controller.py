import re
from Model import Student, Database
from colorama import Fore, Style, init 

init(autoreset=True)

class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def register_student(self, email, password):
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            # print (f"{Fore.RED}        Incorrect email or password format")
            # return "Incorrect email or password format"
            raise ValueError
        else:
            print (f"{Fore.YELLOW}        email and password formats acceptable")
        if email in self.students:
            existing_student = self.students[email]
            print(f"{Fore.RED}        Student {existing_student.name} already registered")
            return "Student already registered."
        name = input("        Name: ")
        if not name:
            print (f"{Fore.RED}        Please enter your given name")
            return "Please enter your given name"
        new_student = Student(name, email, password)
        self.students[email] = new_student
        Database.save_students(self.students)
        print(f"{Fore.YELLOW}        Enrolling Student {name}")
        return "Registration successful."

    def login_student(self, email, password):
        self.students = Database.load_students()
        if not self.is_valid_email(email) or not self.is_valid_password(password):
            # print (f"{Fore.RED}        Incorrect email or password format")
            raise ValueError
            # return "Incorrect email or password format"
        else:
            print (f"{Fore.YELLOW}        email and password formats acceptable")
        student = self.students.get(email)
        if student is None:
            # print(f"{Fore.RED}        Student does not exist")
            raise TypeError
        
        if student.password != password:
            # print(f"{Fore.RED}        Student does not exist")
            raise TypeError
        
        elif student.password == password:
            return student
        
        

    @staticmethod
    def is_valid_email(email):
        return re.match(r"^[a-z]+\.[a-z]+@university\.com$", email)

    @staticmethod
    def is_valid_password(password):
        return re.match(r"^[A-Z][a-zA-Z]{5,}\d{3,}$", password)

class AdminController:
    def __init__(self):
        self.students = Database.load_students()

    def remove_student(self, student_id):
        self.students = Database.load_students()
        if any(s.id == student_id for s in self.students.values()):
            self.students = {email: s for email, s in self.students.items() if s.id != student_id}
            Database.save_students(self.students)
            print(f"{Fore.YELLOW}        Removing student {student_id} Account")
            self.students = Database.load_students()
        else:
            # print(f"{Fore.RED}        Student does not exist")
            raise TypeError

    def partition_students(self):
        self.students = Database.load_students()
        pass_students = [s for s in self.students.values() if self.calculate_average(s) >= 50]
        fail_students = [s for s in self.students.values() if self.calculate_average(s) < 50]
        return {"Pass": pass_students, "Fail": fail_students}

    def group_students(self):
        self.students = Database.load_students()
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
        return f"{Fore.YELLOW}        Student data cleared"