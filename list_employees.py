#List all employees in organization
import mysql.connector

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

# Function to list all employees in the organization along with their department, position, and gender
def list_employees(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, department, position, gender FROM employee_data")
        employees = cursor.fetchall()
        if employees:
            print("\nList of Employees:")
            for employee in employees:
                print(f"Name: {employee['name']}")
                print(f"Department: {employee['department']}")
                print(f"Position: {employee['position']}")
                print(f"Gender: {employee['gender']}")
                print()  # Print a blank line for better readability
        else:
            print("No employees found in the organization.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Main function to execute the list employees functionality
def main():
    connection = create_connection()

    if connection is None:
        print("Failed to connect to the database. Exiting.")
        return

    list_employees(connection)

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute the main function
if __name__ == "__main__":
    main()
