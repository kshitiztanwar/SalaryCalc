"""main class application entry"""

from salary_calc.views.salary_calc_view import SalaryCalcView


# pylint: disable=R0903
# reason: require few public methods
class App:
    """class to instantiate application"""

    def __init__(self):
        self.salary_calc_view = SalaryCalcView()


if __name__ == "__main__":
    APP = App()
