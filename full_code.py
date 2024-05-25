import mysql.connector
import re
import csv
from datetime import datetime,timedelta

class Employee:
    def __init__(self, emp_id, name, age, address, mobile_number, gender, education_details, doj, department, position, salary, current_projects, past_projects, manager, tech_stacks):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.address = address
        self.mobile_number = mobile_number
        self.gender = gender
        self.education_details = education_details
        self.doj = doj
        self.department = department
        self.position = position
        self.salary = salary
        self.current_projects = current_projects
        self.past_projects = past_projects
        self.manager = manager
        self.tech_stacks = tech_stacks
        self.is_delete = 0  # Default value for is_delete

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='EMS_Project',
            user='root',
            password='Nine@123'
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return None

def validate_name(name):
    if not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', name):
        raise ValueError("Invalid name. Please enter alphabets only with single spaces between words.")

def validate_age(age):
    if not (22 <= age <= 55):
        raise ValueError("Invalid age. Please enter an age between 22 and 55.")

def validate_address(address):
    if not re.match(r'^[a-zA-Z0-9\s,.-]+$', address):
        raise ValueError("Invalid address. Please enter alphanumeric characters with special symbols.")

def validate_mobile_number(mobile_number):
    if not re.match(r'^\+91[7-9]\d{9}$', mobile_number):
        raise ValueError("Invalid mobile number. Please enter a valid number starting with +91 followed by 10 digits starting with 7, 8, or 9.")

def validate_gender(gender):
    if gender.lower() not in ["male", "female"]:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")

def validate_education_details(education_details):
    valid_education = ['B.Tech', 'M.Tech', 'BBA', 'MCA', 'Bcom', 'Bsc', 'MBA']
    if education_details not in valid_education:
        raise ValueError("Invalid education details. Please enter valid details such as B.Tech, M.Tech, BBA, MCA, Bcom, Bsc, MBA.")

def validate_doj(doj):
    try:
        datetime.strptime(doj, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date of joining. Please enter date in YYYY-MM-DD format.")

def validate_department(department):
    valid_departments = ['Engineering', 'Finance', 'Sales', 'Management']
    if department not in valid_departments:
        raise ValueError("Invalid department. Please enter one of the following: Engineering, Finance, Sales, Management.")

def validate_position(position):
    valid_positions = ['MTS-I', 'MTS-II', 'MTS-III', 'SDE-I', 'SDE-II', 'SDE-III', 'DA-I', 'DA-II', 'TDA','Manager']
    if position not in valid_positions:
        raise ValueError("Invalid position. Please enter a valid position such as MTS-I, MTS-II, MTS-III, SDE-I, SDE-II, SDE-III, DA-I, DA-II, TDA.")

def validate_salary(salary):
    if salary < 20000:
        raise ValueError("Invalid salary. Please enter a value greater than or equal to 20000.")

def validate_projects(projects):
    valid_projects = ['UberEats', 'Nv-Ops', 'CODA', 'Ad-Ops', 'Excel Ad-In', 'Spry', 'Bargaining Table','Uk Marketplace','INSA drivers','Training']
    project_list = [project.strip() for project in projects.split(',')]
    for project in project_list:
        if project not in valid_projects:
            raise ValueError(f"Invalid project name '{project}'. Please enter valid project names such as {', '.join(valid_projects)}.")

def validate_manager(managers):
    valid_managers = ['Tushar Roy','Adira Daas','Kalvin','Seema','Lavanya Sekhon','Anay vala', 'jivika Agarwal','Pradosh','Prachi','Sambit']
    manager_list = [manager.strip() for manager in managers.split(',')]
    for manager in manager_list:
        if manager not in valid_managers:
            raise ValueError(f"Invalid manager name '{manager}'. Please enter valid manager names such as {', '.join(valid_managers)}.")
            
def validate_tech_stacks(tech_stacks):
    valid_tech_stacks = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Kotlin','SQL','Djang','Flask','HTMl','CSS']
    tech_stack_list = [stack.strip() for stack in tech_stacks.split(',')]
    for stack in tech_stack_list:
        if stack not in valid_tech_stacks:
            raise ValueError(f"Invalid tech stack '{stack}'. Please enter valid tech stacks such as {', '.join(valid_tech_stacks)}.")

def validate_emp_id(emp_id):
    if not emp_id.isdigit():
        raise ValueError("Please enter a valid Employee ID.")

def get_valid_input(prompt, validate_func, data_type=str, *args):
    while True:
        try:
            value = input(prompt)
            if not value:
                raise ValueError("Input cannot be empty.")
            value = data_type(value)
            validate_func(value, *args)
            return value
        except ValueError as ve:
            print(ve)
            retry = input("Do you want to retry (yes/no)? ").strip().lower()
            if retry != 'yes':
                return None

def get_employee_details():
    emp_id = None
    name = get_valid_input("Enter name: ", validate_name)
    age = get_valid_input("Enter age: ", lambda x: validate_age(int(x)), int)
    address = get_valid_input("Enter address: ", validate_address)
    mobile_number = get_valid_input("Enter mobile number: ", validate_mobile_number)
    gender = get_valid_input("Enter gender: ", validate_gender)
    education_details = get_valid_input("Enter education details: ", validate_education_details)
    doj = get_valid_input("Enter date of joining (YYYY-MM-DD): ", validate_doj)
    department = get_valid_input("Enter department: ", validate_department)
    position = get_valid_input("Enter position: ", validate_position)
    salary = get_valid_input("Enter salary: ", lambda x: validate_salary(float(x)), float)
    current_projects = get_valid_input("Enter current projects: ", validate_projects)
    past_projects = get_valid_input("Enter past projects: ", validate_projects)
    manager = get_valid_input("Enter manager name: ", validate_manager)
    tech_stacks = get_valid_input("Enter tech stacks: ", validate_tech_stacks)

    return Employee(emp_id, name, age, address, mobile_number, gender, education_details, doj, department, position, salary, current_projects, past_projects, manager, tech_stacks)

def add_employee_to_db(connection, employee):
    cursor = connection.cursor()
    try:
        sql = """
        INSERT INTO employee_data (name, age, address, mobile_number, gender, education_details, doj, department, position, salary, current_projects, past_projects, manager, tech_stacks, is_delete)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (employee.name, employee.age, employee.address, employee.mobile_number, employee.gender, employee.education_details, employee.doj, employee.department, employee.position, employee.salary, employee.current_projects, employee.past_projects, employee.manager, employee.tech_stacks, employee.is_delete))
        connection.commit()
        print("Employee record inserted successfully")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        connection.rollback()
    finally:
        cursor.close()

#Function to find employee id by name
def find_employee_id_by_name(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT emp_id FROM employee_data WHERE name = %s", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Returning the employee ID
        else:
            print(f"No employee found with the name '{name}'.")
            return None
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        cursor.close()


# Function to view employee details
def view_employee_details(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, age, gender, mobile_number, education_details, department, is_delete FROM employee_data WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        if result:
            if result['is_delete'] == 1:
                print("Employee record is inactive")
            else:
                print("\nEmployee Details:")
                print(f"Name: {result['name']}")
                print(f"Age: {result['age']}")
                print(f"Gender: {result['gender']}")
                print(f"Mobile Number: {result['mobile_number']}")
                print(f"Education Details: {result['education_details']}")
                print(f"Department: {result['department']}")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
            return False
        return True
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        cursor.close()

# Function to update employee information
def update_employee_info(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employee_data WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        
        if result:
            if result['is_delete'] == 1:
                print("Cannot update inactive employee record")
                return
            
            print("\nCurrent Employee Details:")
            for key, value in result.items():
                if key != 'is_delete':
                    print(f"{key}: {value}")

            while True:
                print("\nSelect the information you want to update:")
                print("1. Age")
                print("2. Address")
                print("3. Mobile number")
                print("4. Position")
                print("5. Current Projects")
                print("6. Past Projects")
                print("7. Manager")
                print("8. Exit")

                choice = input("Enter your choice (1-8): ")

                if choice == '1':
                    new_value = get_valid_input("Enter new age: ", validate_age, int)
                    update_field(connection, emp_id, "age", new_value)
                elif choice == '2':
                    new_value = get_valid_input("Enter new address: ", validate_address)
                    update_field(connection, emp_id, "address", new_value)
                elif choice == '3':
                    new_value = get_valid_input("Enter new mobile number: ", validate_mobile_number)
                    update_field(connection, emp_id, "mobile_number", new_value)
                elif choice == '4':
                    new_value = get_valid_input("Enter new position: ", validate_position)
                    update_field(connection, emp_id, "position", new_value)
                elif choice == '5':
                    new_value = get_valid_input("Enter new current projects: ", validate_projects)
                    update_field(connection, emp_id, "current_projects", new_value)
                elif choice == '6':
                    new_value = get_valid_input("Enter new past projects: ", validate_projects)
                    update_field(connection, emp_id, "past_projects", new_value)
                elif choice == '7':
                    new_value = get_valid_input("Enter new manager: ", validate_manager)
                    update_field(connection, emp_id, "manager", new_value)
                elif choice == '8':
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to update a specific field in the employee data
def update_field(connection, emp_id, field_name, new_value):
    cursor = connection.cursor()
    try:
        sql = f"UPDATE employee_data SET {field_name} = %s WHERE emp_id = %s"
        cursor.execute(sql, (new_value, emp_id))
        connection.commit()
        print(f"Employee {field_name} updated successfully")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        connection.rollback()
    finally:
        cursor.close()

# Function to check if an employee exists
def employee_exists(cursor, emp_id):
    cursor.execute("SELECT COUNT(*) FROM employee_data WHERE emp_id = %s", (emp_id,))
    count = cursor.fetchone()[0]
    return count > 0

# Function to mark an employee record as inactive (soft delete)
def soft_delete_employee(connection):
    cursor = connection.cursor()

    try:
        current_date = datetime.now().date()
        one_month_ago = current_date - timedelta(days=30)

        emp_id = get_valid_input("Enter the Employee ID to delete: ", validate_emp_id)
        
        if not employee_exists(cursor, emp_id):
            print(f"No employee found with Employee ID: {emp_id}")
            return

        cursor.execute("UPDATE employee_data SET is_delete = 1 WHERE emp_id = %s AND doj <= %s", (emp_id, one_month_ago))
        connection.commit()
        print("Employee record marked as inactive")
    except mysql.connector.Error as e:
        print(f"Error marking employee record as inactive: {e}")
    finally:
        if connection.is_connected():
            cursor.close()

# Function to list all employees in the organization along with their department, position, and gender
def list_employees(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, department, position, gender FROM employee_data WHERE is_delete = 0")
        employees = cursor.fetchall()
        if employees:
            print("\nList of Active Employees:")
            for employee in employees:
                print(f"Name: {employee['name']}")
                print(f"Department: {employee['department']}")
                print(f"Position: {employee['position']}")
                print(f"Gender: {employee['gender']}")
                print()  # Print a blank line for better readability
        else:
            print("No active employees found in the organization.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to display the total monthly salary of each employee
def display_monthly_salary(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT emp_id, name, position, salary
        FROM employee_data
        WHERE is_delete = 0
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        if employees:
            print("\nMonthly Salary of Active Employees:")
            for employee in employees:
                print(f"Emp_ID: {employee['emp_id']}")
                print(f"Name: {employee['name']}")
                print(f"Monthly Salary: {employee['salary']:.2f}")
                print()  # For an empty line between employees
        else:
            print("No active employees found.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to export employee data to a CSV file
def export_employee_data_to_csv(connection, file_name):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT *
        FROM employee_data
        WHERE is_delete = 0
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        if employees:
            # Extract column names
            fieldnames = employees[0].keys()
            with open(file_name, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for employee in employees:
                    writer.writerow(employee)
            print(f"Employee data exported successfully to '{file_name}'")
        else:
            print("No employee data to export.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()


# Function to import employee data from a CSV file
def import_employee_data_from_csv(connection, csv_file_path):
    try:
        cursor = connection.cursor()
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute("""
                    INSERT INTO employee_data (
                        name, age, address, mobile_number, gender, education_details, doj, 
                        department, position, salary, current_projects, past_projects, manager, tech_stacks, is_delete
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                    row['name'], row['age'], row['address'], row['mobile_number'], row['gender'], row['education_details'], row['doj'],
                    row['department'], row['position'], row['salary'], row['current_projects'], row['past_projects'], row['manager'], row['tech_stacks'], 0
                ))
        connection.commit()
        print(f"Employee data imported from '{csv_file_path}' successfully")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")

# Function to view employee's project details
def view_employee_projects(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, current_projects, past_projects, is_delete FROM employee_data WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        if result:
            if result['is_delete'] == 1:
                print("Employee record is inactive")
            else:
                print("\nEmployee Project Details:")
                print(f"Name: {result['name']}")
                print(f"Current Projects: {result['current_projects']}")
                print(f"Past Projects: {result['past_projects']}")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to update the project details of an employee
def update_employee_projects(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, past_projects, is_delete FROM employee_data WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        if result:
            if result['is_delete'] == 1:
                print("Employee record is inactive")
                return

            print(f"\nEmployee Name: {result['name']}")
            print(f"Past Projects: {result['past_projects']}")
            new_projects = get_valid_input("Enter new current projects: ", validate_project_details)
            if new_projects:
                cursor.execute("UPDATE employee_data SET current_projects = %s WHERE emp_id = %s", (new_projects, emp_id))
                connection.commit()
                print("Employee's current projects updated successfully.")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to view manager details of an employee
def view_manager_details(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT manager, current_projects FROM employee_data WHERE emp_id = %s AND is_delete = 0", (emp_id,))
        result = cursor.fetchone()
        if result:
            manager_name = result['manager']
            cursor.execute("SELECT emp_id, name, current_projects FROM employee_data WHERE manager = %s AND is_delete = 0", (manager_name,))
            mentees = cursor.fetchall()

            print(f"\nManager Name: {manager_name}")
            print(f"Manager's Projects: {result['current_projects']}")

            if mentees:
                print("\nMentees under this Manager:")
                for mentee in mentees:
                    print(f"Employee ID: {mentee['emp_id']}, Name: {mentee['name']}, Current Projects: {mentee['current_projects']}")
            else:
                print("This manager has no mentees.")
        else:
            print(f"Employee id is inactive: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to add tech stacks for an employee 
def add_employee_tech_stack(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, tech_stacks FROM employee_data WHERE emp_id = %s AND is_delete = 0", (emp_id,))
        result = cursor.fetchone()
        if result:
            print(f"\nEmployee Name: {result['name']}")
            print(f"Current Tech Stacks: {result['tech_stacks']}")

            new_tech_stack = get_valid_input("Enter new tech stack to add (only alphabets and commas): ", validate_tech_stack)
            if new_tech_stack:
                updated_tech_stacks = f"{result['tech_stacks']}, {new_tech_stack}" if result['tech_stacks'] else new_tech_stack
                cursor.execute("UPDATE employee_data SET tech_stacks = %s WHERE emp_id = %s AND is_delete = 0", (updated_tech_stacks, emp_id))
                connection.commit()
                print("Tech stacks updated successfully.")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to view tech stacks of Employees
def view_engineering_tech_stack(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, department, tech_stacks FROM employee_data WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        if result:
            print(f"\nEmployee Name: {result['name']}")
            print(f"Department: {result['department']}")
            if result['department'].lower() == 'engineering':
                print(f"Tech Stacks: {result['tech_stacks']}")
            else:
                print("This employee is not in the engineering department.")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to search employees by name using REGEXP for exact word match
def search_employees_by_name(connection, name):
    cursor = connection.cursor(dictionary=True)
    try:
        regex = f"\\b{name}\\b"  # This regex will match 'name' as a whole word
        query = """
        SELECT emp_id, education_details, department, position, gender 
        FROM employee_data 
        WHERE name REGEXP %s AND is_delete = 0
        """
        cursor.execute(query, (regex,))
        results = cursor.fetchall()
        if results:
            print("\nSearch Results:")
            for result in results:
                print(f"Emp_ID: {result['emp_id']}")
                print(f"Education Details: {result['education_details']}")
                print(f"Department: {result['department']}")
                print(f"Position: {result['position']}")
                print(f"Gender: {result['gender']}")
                print("-" * 20)
        else:
            print(f"No employees found matching the name '{name}'")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to search employees by tech stack
def search_employees_by_tech_stack(connection, tech_stack):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT emp_id, name, education_details, gender 
        FROM employee_data 
        WHERE FIND_IN_SET(%s, tech_stacks) > 0 AND is_delete = 0
        """
        cursor.execute(query, (tech_stack,))
        results = cursor.fetchall()
        if results:
            print("\nSearch Results:")
            for result in results:
                print(f"Emp_ID: {result['emp_id']}")
                print(f"Name: {result['name']}")
                print(f"Education Details: {result['education_details']}")
                print(f"Gender: {result['gender']}")
                print("-" * 20)
        else:
            print(f"No employees found with tech stack '{tech_stack}'")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to search employees by project name
def search_employees_by_project_name(connection, project_name):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT emp_id, name
        FROM employee_data
        WHERE current_projects LIKE %s AND is_delete = 0
        """
        cursor.execute(query, (f'%{project_name}%',))
        results = cursor.fetchall()
        if results:
            print("\nSearch Results:")
            for result in results:
                print(f"Emp_ID: {result['emp_id']}")
                print(f"Name: {result['name']}")
                print("-" * 20)
        else:
            print(f"No employees found associated with project '{project_name}'")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Function to fetch and sort employees by salary
def sort_employees_by_salary(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT emp_id, name, position, salary
        FROM employee_data
        WHERE is_delete = 0
        ORDER BY salary DESC
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        if employees:
            print("\nEmployees sorted by salary:")
            for employee in employees:
                print(f"Emp_ID: {employee['emp_id']}")
                print(f"Name: {employee['name']}")
                print(f"Salary: {employee['salary']}")
                print()  # For an empty line between employees
        else:
            print("No employees found.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Main function
def main():
    connection = create_connection()
    if connection is None:
        return
        
    while True:
        print("\nEmployee Management System")
        print("1. Add new employee")
        print("2. Get Employee id by Name")
        print("3. View employee details")
        print("4. Update employee information")
        print("5. Delete employee record (soft delete)")
        print("6. View employee project details")
        print("7. Update employee project details")
        print("8. List all employees")
        print("9. Total monthly salary of employees")
        print("10. View manager details")
        print("11. Add tech stacks for employees")
        print("12. View employee's known tech stack")
        print("13. Search employees by name")
        print("14. Search employees by tech stacks")
        print("15. Search employees by project name")
        print("16. Sort Employees by Salary")
        print("17. Export employee data to a CSV file")
        print("18. Import employee data from a CSV file")
        print("19. Exit")

        choice = input("Enter your choice (1-19): ")

        if choice == '1':
            employee = get_employee_details()
            add_employee_to_db(connection, employee)
        elif choice == '2':
            name = input("Enter the name of the employee: ")
            emp_id = find_employee_id_by_name(connection, name)
            if emp_id:
                print(f"Employee ID for '{name}' is {emp_id}.")
        elif choice == '3':
            emp_id = get_valid_input("Enter Employee ID to view details: ", validate_emp_id)
            view_employee_details(connection, emp_id)
        elif choice == '4':
            emp_id = get_valid_input("Enter Employee ID to update: ", validate_emp_id)
            update_employee_info(connection, emp_id)
        elif choice == '5':
            soft_delete_employee(connection)
        elif choice == '6':
            emp_id = get_valid_input("Enter Employee ID to view project details: ", validate_emp_id)
            view_employee_projects(connection, emp_id)
        elif choice == '7':
            emp_id = get_valid_input("Enter Employee ID to update project details: ", validate_emp_id)
            update_employee_projects(connection, emp_id)
        elif choice == '8':
            list_employees(connection)
        elif choice == '9':
            display_monthly_salary(connection)
        elif choice == '10':
            emp_id = get_valid_input("Enter Employee ID to view manager details: ", validate_emp_id)
            view_manager_details(connection, emp_id)
        elif choice == '11':
            emp_id = get_valid_input("Enter Employee ID to add tech stacks: ", validate_emp_id)
            add_employee_tech_stack(connection, emp_id)
        elif choice == '12':
            emp_id = get_valid_input("Enter Employee ID to view tech stack: ", validate_emp_id)
            view_engineering_tech_stack(connection, emp_id)
        elif choice == '13':
            name = input("Enter the name to search: ").strip()
            search_employees_by_name(connection, name)
        elif choice == '14':
            tech_stack = get_valid_input("Enter the tech stack to search: ", validate_tech_stacks)
            search_employees_by_tech_stack(connection, tech_stack)
        elif choice == '15':
            project_name = get_valid_input("Enter the project name to search: ", validate_projects)
            search_employees_by_project_name(connection, project_name)
        elif choice == '16':
            sort_employees_by_salary(connection)
        elif choice == '17':
            export_employee_data_to_csv(connection, 'employee_data.csv')
        elif choice == '18':
            csv_file_path = input("Enter the path to the CSV file: ").strip()
            import_employee_data_from_csv(connection, csv_file_path)
        elif choice == '19':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    connection.close()

if __name__ == "__main__":
    main()
