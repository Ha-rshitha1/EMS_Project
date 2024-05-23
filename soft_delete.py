#Soft Delete
import mysql.connector
from mysql.connector import Error
import datetime

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

# Validation function for employee ID
def validate_emp_id(emp_id):
    if not emp_id.isdigit():
        raise ValueError("Invalid Employee ID. Please enter numerics only.")

# Function to get valid input from user
def get_valid_input(prompt, validate_func):
    while True:
        try:
            value = input(prompt)
            validate_func(value)
            return value
        except ValueError as ve:
            print(ve)
            retry = input("Do you want to retry (yes/no)? ")
            if retry.lower() != 'yes':
                return None

# Function to check if an employee exists
def employee_exists(cursor, emp_id):
    cursor.execute("SELECT COUNT(*) FROM employee_data WHERE emp_id = %s", (emp_id,))
    count = cursor.fetchone()[0]
    return count > 0

# Function to delete employee records who worked less than 1 month
def delete_inactive_employees(connection):
    cursor = connection.cursor()

    try:
        # Calculate today's date
        current_date = datetime.date.today()
        # Calculate the date 1 month ago
        one_month_ago = current_date - datetime.timedelta(days=30)

        while True:
            # Ask for the employee ID to delete
            employee_id = get_valid_input("Enter the Employee ID to delete: ", validate_emp_id)
            if employee_id is None:
                return

            # Check if the employee exists
            if not employee_exists(cursor, employee_id):
                print(f"No employee found with Employee ID: {employee_id}")
                retry = input("Do you want to retry (yes/no)? ")
                if retry.lower() != 'yes':
                    return
            else:
                break

        # Update the 'is_delete' column to mark the employee record as inactive
        cursor.execute("UPDATE employee_data SET is_delete = 1 WHERE doj <= %s AND emp_id = %s", (one_month_ago, employee_id))
        connection.commit()
        print("Employee record marked as inactive")
    except mysql.connector.Error as e:
        print(f"Error marking employee record as inactive: {e}")
    finally:
        if connection.is_connected():
            cursor.close()

# Main function to execute the soft delete functionality
def main():
    connection = create_connection()

    if connection is None:
        print("Failed to connect to the database. Exiting.")
        return

    delete_inactive_employees(connection)

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute the main function
if __name__ == "__main__":
    main()
