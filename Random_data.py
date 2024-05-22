import random
from faker import Faker
import datetime
import pandas as pd

fake = Faker('en_IN')

def random_education():
    return random.choice(['B.Tech', 'M.Tech', 'MBA', 'BBA', 'B.Sc', 'B.Com'])

def random_doj():
    start_date = datetime.date(2023, 5, 1)
    end_date = datetime.date(2024, 5, 5)
    return fake.date_between(start_date=start_date, end_date=end_date)

def assign_department(education):
    if education in ['B.Tech', 'M.Tech']:
        return 'Engineering'
    elif education in ['MBA', 'BBA']:
        return 'Management'
    elif education == 'B.Com':
        return 'Finance'
    elif education == 'B.Sc':
        return 'Sales'

def random_position():
    return random.choice(["Manager", "MTS I", "MTS II", "MTS III", "SDE I", "SDE II", "SDE III", "TDA", "DA-I", "DA-II", "DA-III", "SM-DEO"])

def random_salary(position, current_projects):
    if "Training" in current_projects:
        return 20000
    elif position == "Manager":
        return random.randint(125000, 200000)
    else:
        return random.randint(45000, 100000)

def random_projects():
    return random.sample(["Spry", "Bargaining Table", "CODA", "INSA Drivers", "Excel Ad-In", "GDW", "UK MarketPlace", "Socion", "U4B", "Bingo"], random.randint(1, 2))

def random_tech_stacks():
    return random.sample(["Python", "Java", "C++", "JavaScript", "SQL", "HTML/CSS", "Django", "Flask", "React", "Angular"], random.randint(1, 3))

# Generate employees
employees = []
mobile_numbers = set()
names = []

for emp_id in range(1, 101):
    gender = random.choice(["Male", "Female"])
    name = fake.name_male() if gender == "Male" else fake.name_female()
    names.append(name)
    age = random.randint(22, 55)
    address = fake.address().replace('\n', ', ')
    
    # Ensure unique mobile numbers
    while True:
        mobile_number = f"+91{random.choice([7, 8, 9])}{random.randint(100000000, 999999999)}"
        if mobile_number not in mobile_numbers:
            mobile_numbers.add(mobile_number)
            break
    
    education = random_education()
    doj = random_doj()
    department = assign_department(education)
    position = random_position()
    
    current_projects = ["Training"] if random.choice([True, False]) else random_projects()
    salary = random_salary(position, current_projects)
    
    employee = {
        "emp_id": emp_id,
        "name": name,
        "age": age,
        "address": address,
        "mobile_number": mobile_number,
        "gender": gender,
        "education_details": education,
        "doj": doj,
        "department": department,
        "position": position,
        "salary": salary,
        "current_projects": ', '.join(current_projects),
        "past_projects": '' if "Training" in current_projects else ', '.join(random_projects()),
        "manager": '',  # This will be updated later
        "tech_stacks": ', '.join(random_tech_stacks()),
        "is_delete": 0
    }
    
    employees.append(employee)

# Select 20 random employee names to be managers
manager_names = random.sample(names, 20)

# Assign manager names to the employees
for employee in employees:
    employee["manager"] = random.choice(manager_names)

# Create a DataFrame
df = pd.DataFrame(employees)

# Save to CSV
#df.to_csv("/home/kandagadla.harshitha@nineleaps.com/Downloads/employee1_data.csv", index=False)

# Print the first 5 records
print(df.head())
