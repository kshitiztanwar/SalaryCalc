"""edit entry controller"""
from salary_calc.model.employee import read_all_employees_from_file, Employee, \
    update_employees_to_file


# pylint: disable=R0903
# reason: require too few public methods
class EditEntryController:
    """controller for edit entry view"""

    def __init__(self, edit_entry_view):
        self.edit_entry_view = edit_entry_view

    # pylint: disable=W0613
    # reason: require event param for callback
    def save_button_callback(self, event):
        """callback for save button"""

        new_emp_name = str(self.edit_entry_view.name_entry.get())
        new_emp_salary = int(self.edit_entry_view.salary_entry.get())
        new_emp_type = str(self.edit_entry_view.type_options.get())
        new_emp_id = str(self.edit_entry_view.employee.emp_id)
        new_emp = Employee(new_emp_name, new_emp_salary, new_emp_type, new_emp_id)

        all_employees = read_all_employees_from_file()
        for emp in all_employees:
            if emp.emp_id == new_emp_id:
                all_employees.remove(emp)

        all_employees.append(new_emp)
        update_employees_to_file(all_employees)

        self.edit_entry_view.edit_win.destroy()
