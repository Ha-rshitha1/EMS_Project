#Update Employee Information
import mysql.connector
import re

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

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='EMS',  # Replace with your database name
            user='root',
            password='Nine@123'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return None

# Validation functions
def validate_name(name):
    if not name.isalpha():
        raise ValueError("Invalid name. Please enter alphabets only.")

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
    if not re.match(r'^[a-zA-Z\s,.-]+$', education_details):
        raise ValueError("Invalid education details. Please enter valid details.")

def validate_doj(doj):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', doj):
        raise ValueError("Invalid date of joining. Please enter date in YYYY-MM-DD format.")

def validate_department(department):
    if not re.match(r'^[a-zA-Z\s]+$', department):
        raise ValueError("Invalid department. Please enter alphabets only.")

def validate_position(position):
    if not re.match(r'^[a-zA-Z\s,.-]+$', position):
        raise ValueError("Invalid position. Please enter valid position details.")

def validate_salary(salary):
    if salary < 20000:
        raise ValueError("Invalid salary. Please enter a value greater than or equal to 20000.")

def validate_projects(projects):
    if not re.match(r'^[a-zA-Z\s,.-]+$', projects):
        raise ValueError("Invalid projects. Please enter valid project details.")

def validate_manager(manager):
    if not re.match(r'^[a-zA-Z\s]+$', manager):
        raise ValueError("Invalid manager name. Please enter alphabets only.")

def validate_tech_stacks(tech_stacks):
    if not re.match(r'^[a-zA-Z\s,.-]+$', tech_stacks):
        raise ValueError("Invalid tech stacks. Please enter valid tech stacks.")

def validate_emp_id(emp_id):
    if not emp_id.isdigit():
        raise ValueError("Please enter a valid Employee ID.")

# Function to get valid input from user
def get_valid_input(prompt, validate_func, data_type=str):
    while True:
        try:
            value = input(prompt)
            value = data_type(value)
            validate_func(value)
            return value
        except ValueError as ve:
            print(ve)

# Function to update employee information
def update_employee_info(connection, emp_id):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employee_data WHERE emp_id = %s AND is_delete = 0", (emp_id,))
        result = cursor.fetchone()
        
        if result:
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
                    new_value = get_valid_input("Enter new manager name: ", validate_manager)
                    update_field(connection, emp_id, "manager", new_value)
                elif choice == '8':
                    print("Exiting update menu.")
                    return False  # Exit update process
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.")
        else:
            print(f"No employee found with Emp_ID: {emp_id}")
            return True  # Prompt to retry

    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
        return True  # Prompt to retry
    finally:
        cursor.close()

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

# Main function to execute the update employee information functionality
def main():
    connection = create_connection()

    if connection is None:
        print("Failed to connect to the database. Exiting.")
        return

    while True:
        emp_id = get_valid_input("Enter Employee ID: ", validate_emp_id)
        if emp_id == "exit":
            break
        
        should_retry = update_employee_info(connection, emp_id)
        
        if not should_retry:
            break

        retry = input("Do you want to retry(yes/no): ").strip().lower()
        if retry != 'yes':
            break

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute the main function
if __name__ == "__main__":
    main()
