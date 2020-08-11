"""salary calculator view"""

from tkinter import Tk, Scrollbar, Button, Label, VERTICAL, LEFT, RIGHT, TOP, Y
from tkinter.ttk import Treeview
from salary_calc.app_constants import ATTACH_BUTTON_TEXT, DARK_GREEN, \
    WHITE, CALC_AND_SAVE_BUTTON_TEXT, ROOT_TITLE, \
    ROOT_WIDTH, ROOT_HEIGHT, NAME_COLUMN_WIDTH, \
    SALARY_COLUMN_WIDTH, NAME_COLUMN_HEADER, SALARY_COLUMN_HEADER, \
    DEFAULT_BUTTON_SIZE, DEFAULT_BUTTON_Y_PADDING, ATTACH_LABEL_Y_PADDING, TYPE_COLUMN_WIDTH, \
    TYPE_COLUMN_HEADER, ATTACH_LABEL_SIZE
from salary_calc.controllers.salary_calc_controller import SalaryCalcController


# pylint: disable=R0902,R0903
# reason: require many instance attributes and few public methods
class SalaryCalcView:
    """class to instantiate salary calculator view"""

    def __init__(self):
        self.salary_calc_controller = SalaryCalcController(self)
        self.root = Tk()
        self.tree_view = Treeview(self.root, show="headings", height=100)
        self.scroll_bar = Scrollbar(self.root, orient=VERTICAL, command=self.tree_view.yview)
        self.attach_button = Button(self.root, text=ATTACH_BUTTON_TEXT)
        self.attach_label = \
            Label(self.root, bg=DARK_GREEN, foreground=WHITE, wraplength=ATTACH_LABEL_SIZE)
        self.calc_save_button = Button(self.root, text=CALC_AND_SAVE_BUTTON_TEXT)
        self.calc_save_label = Label(self.root, bg=DARK_GREEN, foreground=WHITE)
        self.attached_file_path = ""
        self._config_widgets()
        self._pack_widgets()
        self.root.mainloop()

    def _config_widgets(self):
        """configure on screen widgets"""

        # configure root
        self.root.config(background=DARK_GREEN)
        self.root.title(ROOT_TITLE)
        self.root.geometry("{}x{}".format(ROOT_HEIGHT, ROOT_WIDTH))
        self.root.resizable(False, False)
        self.root.bind("<FocusIn>", self.salary_calc_controller.handle_focus)

        # configure tree_view
        self.tree_view["columns"] = ("name", "salary", "type")
        self.tree_view.column("name", width=NAME_COLUMN_WIDTH)
        self.tree_view.column("salary", width=SALARY_COLUMN_WIDTH)
        self.tree_view.column("type", width=TYPE_COLUMN_WIDTH)
        self.tree_view.heading("name", text=NAME_COLUMN_HEADER)
        self.tree_view.heading("salary", text=SALARY_COLUMN_HEADER)
        self.tree_view.heading("type", text=TYPE_COLUMN_HEADER)
        self.salary_calc_controller.refresh_tree_view()
        self.tree_view.configure(yscrollcommand=self.scroll_bar.set)
        self.tree_view.bind("<Double-1>",
                            self.salary_calc_controller.tree_view_double_click_callback)
        self.tree_view.bind("<Key>",
                            self.salary_calc_controller.tree_view_delete_callback)

        # configure attach_button
        self.attach_button.config(width=DEFAULT_BUTTON_SIZE)
        self.attach_button.bind("<ButtonRelease-1>",
                                self.salary_calc_controller.attach_file_button_callback)

        # configure calc_save_button
        self.calc_save_button.config(width=DEFAULT_BUTTON_SIZE)
        self.calc_save_button.bind("<ButtonRelease-1>",
                                   self.salary_calc_controller.calc_and_save_button_callback)

    def _pack_widgets(self):
        """pack widgets on screen"""

        self.tree_view.pack(side=LEFT)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.attach_button.pack(side=TOP, pady=DEFAULT_BUTTON_Y_PADDING)
        self.attach_label.pack(side=TOP, pady=ATTACH_LABEL_Y_PADDING)
        self.calc_save_button.pack(side=TOP, pady=DEFAULT_BUTTON_Y_PADDING)
        self.calc_save_label.pack(side=TOP)
