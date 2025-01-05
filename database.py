import sqlite3
from faker import Faker
import random

# Initialize Faker for generating fake data
faker = Faker()

# Create an SQLite database and connect
conn = sqlite3.connect('college_students.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    branch TEXT NOT NULL,
    year INTEGER NOT NULL,
    gpa REAL NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL
)
''')

# List of branches
branches = ['Computer Science', 'Mechanical Engineering', 'Electrical Engineering',
            'Civil Engineering', 'Electronics and Communication', 'AI and ML']

# Gender options
genders = ['Male', 'Female', 'Other']

# Function to generate random student data
def generate_student():
    name = faker.name()
    age = random.randint(18, 25)
    gender = random.choice(genders)
    branch = random.choice(branches)
    year = random.randint(1, 4)  # Assuming a 4-year course
    gpa = round(random.uniform(6.0, 10.0), 2)  # GPA between 6.0 and 10.0
    email = faker.unique.email()
    phone = faker.unique.phone_number()
    return name, age, gender, branch, year, gpa, email, phone

# Insert fake students into the database
def populate_database(num_students):
    for _ in range(num_students):
        student_data = generate_student()
        cursor.execute('''
        INSERT INTO students (name, age, gender, branch, year, gpa, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', student_data)
    conn.commit()

# Populate the database with 100 students
populate_database(100)

# Fetch and display some student records for verification
cursor.execute('SELECT * FROM students LIMIT 10')
students = cursor.fetchall()
print("Sample Student Records:")
for student in students:
    print(student)

# Close the database connection
conn.close()
