#Import employee_data from csv file
import mysql.connector
import csv

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

# Function to import employee data from a CSV file
def import_employee_data_from_csv(connection, csv_file_path):
    cursor = connection.cursor()
    try:
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
                    row['department'], row['position'], row['salary'], row['current_projects'], row['past_projects'], row['manager'], row['tech_stacks'], row['is_delete']
                ))
        connection.commit()
        print(f"Employee data imported from '{csv_file_path}' successfully")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

# Main function to execute the import functionality
def main():
    connection = create_connection()

    if connection is None:
        print("Failed to connect to the database. Exiting.")
        return

    csv_file_path = input("Enter the path to the CSV file: ").strip()
    import_employee_data_from_csv(connection, csv_file_path)

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute the main function
if __name__ == "__main__":
    main()
