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
            print(f"No employee found with Emp_ID: {emp_id}")
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
