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