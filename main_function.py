# Main function
def main():
    connection = create_connection()
    if connection is None:
        return

    while True:
        print("\nEmployee Management System")
        print("1. Add new employee")
        print("2. View employee details")
        print("3. Update employee information")
        print("4. Delete employee record (soft delete)")
        print("5. View employee project details")
        print("6. Update employee project details")
        print("7. List all employees")
        print("8. Total monthly salary of employees")
        print("9. View manager details")
        print("10. Add tech stacks for employees")
        print("11. View employee's known tech stack")
        print("12. Search employees by name")
        print("13. Search employees by tech stacks")
        print("14. Search employees by project name")
        print("15. Sort Employees by Salary")
        print("16. Export employee data to a CSV file")
        print("17. Import employee data from a CSV file")
        print("18. Exit")

        choice = input("Enter your choice (1-18): ")

        if choice == '1':
            employee = get_employee_details()
            add_employee_to_db(connection, employee)
        elif choice == '2':
            emp_id = get_valid_input("Enter Employee ID to view details: ", validate_emp_id)
            view_employee_details(connection, emp_id)
        elif choice == '3':
            emp_id = get_valid_input("Enter Employee ID to update: ", validate_emp_id)
            update_employee_info(connection, emp_id)
        elif choice == '4':
            soft_delete_employee(connection)
        elif choice == '5':
            emp_id = get_valid_input("Enter Employee ID to view project details: ", validate_emp_id)
            view_employee_projects(connection, emp_id)
        elif choice == '6':
            emp_id = get_valid_input("Enter Employee ID to update project details: ", validate_emp_id)
            update_employee_projects(connection, emp_id)
        elif choice == '7':
            list_employees(connection)
        elif choice == '8':
            display_monthly_salary(connection)
        elif choice == '9':
            emp_id = get_valid_input("Enter Employee ID to view manager details: ", validate_emp_id)
            view_manager_details(connection, emp_id)
        elif choice == '10':
            emp_id = get_valid_input("Enter Employee ID to add tech stacks: ", validate_emp_id)
            add_employee_tech_stack(connection, emp_id)
        elif choice == '11':
            emp_id = get_valid_input("Enter Employee ID to view tech stack: ", validate_emp_id)
            view_engineering_tech_stack(connection, emp_id)
        elif choice == '12':
            name = input("Enter the name to search: ").strip()
            search_employees_by_name(connection, name)
        elif choice == '13':
            tech_stack = get_valid_input("Enter the tech stack to search: ", validate_tech_stack)
            search_employees_by_tech_stack(connection, tech_stack)
        elif choice == '14':
            project_name = get_valid_input("Enter the project name to search: ", validate_projects)
            search_employees_by_project_name(connection, project_name)
        elif choice == '15':
            sort_employees_by_salary(connection)
        elif choice == '16':
            export_employee_data_to_csv(connection, 'employee_data.csv')
        elif choice == '17':
            csv_file_path = input("Enter the path to the CSV file: ").strip()
            import_employee_data_from_csv(connection, csv_file_path)
        elif choice == '18':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    connection.close()

if __name__ == "__main__":
    main()
