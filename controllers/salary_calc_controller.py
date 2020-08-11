"""salary calculator controller"""
from tkinter import END
from tkinter.filedialog import askopenfile
from salary_calc.app_constants import DEFAULT_LABEL_TEXT, ATTACH_ATTENDANCE_SHEET_MSG, SAVED_MSG, \
    BACKSPACE_KEYSYM
from salary_calc.model.employee import read_all_employees_from_file, update_employees_to_file, \
    get_employee_by_id_from_file, get_default_new_employee
from salary_calc.model.salary_calc import calc_save_salaries
from salary_calc.views.edit_entry_view import EditEntryView


class SalaryCalcController:
    """controller for salary calc view"""

    def __init__(self, salary_calc_view):
        self.salary_calc_view = salary_calc_view

    # pylint: disable=W0613
    # reason: require event param for callback
    def attach_file_button_callback(self, event):
        """callback for attach file button"""

        file = askopenfile()
        file_path = file.name
        file_path_arr = file_path.split("/")
        file_name = file_path_arr[len(file_path_arr) - 1]
        self.salary_calc_view.attach_label.configure(text=file_name)
        self.salary_calc_view.calc_save_label.configure(text=DEFAULT_LABEL_TEXT)
        self.salary_calc_view.attached_file_path = file_path

    # pylint: disable=W0613
    # reason: require event param for callback
    def calc_and_save_button_callback(self, event):
        """callback for calc and save button"""

        attach_label_text = self.salary_calc_view.attach_label.cget("text")
        if attach_label_text == DEFAULT_LABEL_TEXT:
            self.salary_calc_view.calc_save_label.configure(text=ATTACH_ATTENDANCE_SHEET_MSG)
        else:
            self.salary_calc_view.calc_save_label.configure(text=SAVED_MSG)
            self.salary_calc_view.attach_label.configure(text=DEFAULT_LABEL_TEXT)
            calc_save_salaries(self.salary_calc_view.attached_file_path)

    # pylint: disable=W0613
    # reason: require event param for callback
    def tree_view_double_click_callback(self, event):
        """callback for double click on tree view"""

        item = self.salary_calc_view.tree_view.identify("item", event.x, event.y)
        employee = get_employee_by_id_from_file(item)
        if employee is None:
            EditEntryView(get_default_new_employee())
        else:
            EditEntryView(employee)

    def tree_view_delete_callback(self, event):
        """callback for delete button on tree view"""

        if event.keysym == BACKSPACE_KEYSYM:
            employees = read_all_employees_from_file()
            for item in self.salary_calc_view.tree_view.selection():
                for emp in employees:
                    if emp.emp_id == str(item):
                        employees.remove(emp)
            update_employees_to_file(employees)
            self.refresh_tree_view()

    def refresh_tree_view(self):
        """refreshes tree view data with latest data from file"""

        tree_view = self.salary_calc_view.tree_view
        tree_view.delete(*tree_view.get_children())
        employees = read_all_employees_from_file()
        for emp in employees:
            values = (emp.emp_name, emp.emp_salary, emp.emp_type)
            tree_view.insert("", END, id=emp.emp_id, values=values)

    # pylint: disable=W0613
    # reason: require event param for callback
    def handle_focus(self, event):
        """refreshes updated elements on focus"""

        self.refresh_tree_view()
