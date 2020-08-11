"""view for edit entry"""

from tkinter import Toplevel, Label, Entry, Button, END, StringVar, OptionMenu
from salary_calc.app_constants import EDIT_ENTRY_NAME_LABEL_TEXT, EDIT_ENTRY_SAVE_LABEL_TEXT, \
    DARK_GREEN, WHITE, EDIT_ENTRY_SAVE_BUTTON, EDIT_WIN_TITLE, EDIT_ENTRY_TYPE_LABEL_TEXT, \
    DRIVER_TYPE, REGULAR_TYPE, OPERATOR_TYPE
from salary_calc.controllers.edit_entry_controller import EditEntryController


# pylint: disable=R0902,R0903
# reason: require many instance attributes and few public methods
class EditEntryView:
    """class to instantiate edit entry view"""

    def __init__(self, employee):
        self.employee = employee
        self.edit_entry_controller = EditEntryController(self)
        self.edit_win = Toplevel()
        self.name_label = \
            Label(self.edit_win, text=EDIT_ENTRY_NAME_LABEL_TEXT, bg=DARK_GREEN, foreground=WHITE)
        self.name_entry = Entry(self.edit_win)
        self.salary_label = \
            Label(self.edit_win, text=EDIT_ENTRY_SAVE_LABEL_TEXT, bg=DARK_GREEN, foreground=WHITE)
        self.salary_entry = Entry(self.edit_win)
        self.type_label = \
            Label(self.edit_win, text=EDIT_ENTRY_TYPE_LABEL_TEXT, bg=DARK_GREEN, foreground=WHITE)
        self.type_options = StringVar(self.edit_win)
        self.type_menu = \
            OptionMenu(self.edit_win, self.type_options, OPERATOR_TYPE, REGULAR_TYPE, DRIVER_TYPE)
        self.space_label = Label(self.edit_win, text="       ", bg=DARK_GREEN)
        self.save_button = Button(self.edit_win, text=EDIT_ENTRY_SAVE_BUTTON)
        self._config_widgets()
        self._pack_widgets()

    def _config_widgets(self):
        """configure view widgets"""

        # configure edit_win
        self.edit_win.title(EDIT_WIN_TITLE)
        self.edit_win.attributes("-topmost", True)
        self.edit_win.resizable(False, False)
        self.edit_win.config(background=DARK_GREEN)

        # configure name_entry
        self.name_entry.insert(END, self.employee.emp_name)

        # configure salary_entry
        self.salary_entry.insert(END, self.employee.emp_salary)

        # configure type_menu
        self.type_options.set(self.employee.emp_type)

        # configure save_button
        self.save_button.bind("<ButtonRelease-1>", self.edit_entry_controller.save_button_callback)

    def _pack_widgets(self):
        """pack widgets on screen"""

        row = 0
        self.name_label.grid(row=row, column=1)
        self.name_entry.grid(row=row, column=2)
        self.salary_label.grid(row=row, column=3)
        self.salary_entry.grid(row=row, column=4)
        self.type_label.grid(row=row, column=5)
        self.type_menu.grid(row=row, column=6)
        self.space_label.grid(row=row, column=7)
        self.save_button.grid(row=row, column=8)
