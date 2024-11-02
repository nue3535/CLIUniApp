import random
import pickle
import os
from colorama import Fore, Style, init

init(autoreset=True)

# Subject class
class Subject:
    def __init__(self, id):
        self.id = id
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

# Student class
class Student:
    def __init__(self, name, email, password):
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def enroll_subject(self, subject_id):
        if len(self.subjects) < 4:
            new_subject = Subject(subject_id)
            self.subjects.append(new_subject)
            return f"{Fore.YELLOW}                Enrolling in Subject-{subject_id}"
        
    def remove_subject(self, subject_id):
        self.subjects = [s for s in self.subjects if s.id != subject_id]

    def view_enrollments(self):
        return [(subject.id, subject.mark, subject.grade) for subject in self.subjects]

    def change_password(self, new_password):
        self.password = new_password

# Database class
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
        with open(Database.FILE_NAME, 'wb') as file:
            pickle.dump({}, file)
        
        