#Total Monthly salary of a employee
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
            print("\nMonthly Salary of Each Employee:")
            for employee in employees:
                print(f"Emp_ID: {employee['emp_id']}")
                print(f"Name: {employee['name']}")
                print(f"Monthly Salary: {employee['salary']:.2f}")
                print()  # For an empty line between employees
        else:
            print("No employees found.")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Main function to execute the monthly salary display
def main():
    connection = create_connection()

    if connection is None:
        print("Failed to connect to the database. Exiting.")
        return

    display_monthly_salary(connection)

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute the main function
if __name__ == "__main__":
    main()
