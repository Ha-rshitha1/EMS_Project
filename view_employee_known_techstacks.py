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

# Function to search employees by name
def search_employees_by_name(connection, name):
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT emp_id, education_details, department, position, gender 
        FROM employee_data 
        WHERE name LIKE %s AND is_delete = 0
        """
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()
        if results:
            print("\nSearch Results:")
            for result in results:
                print(f"Emp_ID: {result['emp_id']}")
                print(f"Education Details: {result['education_details']}")
                print(f"Department: {result['department']}")
                #print(f"Position: {result['position']}")
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
