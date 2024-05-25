
CREATE TABLE employee_data (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    address VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    education_details ENUM('B.Tech', 'M.Tech', 'BBA', 'MCA', 'Bcom', 'Bsc', 'MBA') NOT NULL,
    doj DATE NOT NULL,
    department ENUM('Engineering', 'Finance', 'Sales', 'Management') NOT NULL,
    position ENUM('MTS-I', 'MTS-II', 'MTS-III', 'SDE-I', 'SDE-II', 'SDE-III', 'DA-I', 'DA-II', 'TDA', 'Manager') NOT NULL,
    salary DECIMAL(10, 2) NOT NULL CHECK (salary >= 20000),
    current_projects VARCHAR(255),
    past_projects VARCHAR(255),
    manager VARCHAR(100),
    tech_stacks VARCHAR(255),
    is_delete BOOLEAN DEFAULT 0
);

