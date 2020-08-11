"""employee objects and manager"""
import uuid

from salary_calc.app_constants import OPERATOR_TYPE
from salary_calc.model import salary_calc


# pylint: disable=R0903
# reason: require few public methods
class Employee:
    """object to represent employee"""

    def __init__(self, emp_name, emp_salary, emp_type, emp_id):
        self.emp_name = emp_name
        self.emp_salary = emp_salary
        self.emp_type = emp_type
        self.emp_id = emp_id


def read_all_employees_from_file():
    """reads all employee objects from file"""

    data = salary_calc.get_salaries()
    employees = []

    for employee in data["employees"]:
        emp_name = employee["name"]
        emp_salary = employee["salary"]
        emp_type = employee["type"]
        emp_id = employee["id"]
        employees.append(Employee(emp_name, emp_salary, emp_type, emp_id))

    return employees


def update_employees_to_file(employees):
    """updates current employee objects in file"""

    salary_obj = {"employees": []}

    for emp in employees:
        emp_obj = {"name": emp.emp_name,
                   "salary": emp.emp_salary,
                   "type": emp.emp_type,
                   "id": emp.emp_id}
        salary_obj["employees"].append(emp_obj)

    salary_calc.save_salaries(salary_obj)


def get_employee_by_id_from_file(emp_id):
    """gets employee object by id"""

    employees = read_all_employees_from_file()

    for employee in employees:
        if employee.emp_id == emp_id:
            return employee

    return None


def get_default_new_employee():
    """generate default new employee"""

    emp_name = ""
    emp_salary = 0
    emp_type = OPERATOR_TYPE
    emp_id = str(uuid.uuid4())

    return Employee(emp_name, emp_salary, emp_type, emp_id)


def employee_exists(emp_id):
    """check if employee is present from file"""

    employee = get_employee_by_id_from_file(emp_id)

    return employee is not None
