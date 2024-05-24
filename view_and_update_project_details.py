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