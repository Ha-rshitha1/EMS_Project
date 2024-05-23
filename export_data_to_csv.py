#Export employee data to a csv file
import mysql.connector
import csv

def export_employee_data_to_csv(filename):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='EMS',  # Replace with your database name
            user='root',
            password='Nine@123'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to fetch employee data
        cursor.execute("SELECT * FROM employee_data")

        # Fetch all rows of the result
        rows = cursor.fetchall()

        # Write the data to a CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow([i[0] for i in cursor.description])
            # Write each row of data
            for row in rows:
                writer.writerow(row)

        print(f"Employee data exported to '{filename}' successfully")

    except mysql.connector.Error as e:
        print(f"Error: '{e}'")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Example usage:
export_employee_data_to_csv('employee1_data.csv')
