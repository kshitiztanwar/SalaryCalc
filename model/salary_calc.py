"""salary calculator"""

import os
import sys
from datetime import date
from calendar import monthrange
import json
import xlwt
from xlwt import Formula
from salary_calc.app_constants import SALARY_FILE_PATH, DEFAULT_SHEET_NAME, PATH_TO_EXE
from salary_calc.model.attendance import AttendanceManager


def get_salaries():
    """get salaries from file"""

    with open(SALARY_FILE_PATH) as file:
        data = json.load(file)
    return data


def save_salaries(data):
    """save updated salaries to file"""

    with open(SALARY_FILE_PATH, "w") as file:
        json.dump(data, file, indent=2)


def calc_save_salaries(path):
    """creates and saves excel file with calculated salaries"""

    attendance_man = AttendanceManager(path)
    attendances = attendance_man.attendances

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(DEFAULT_SHEET_NAME)
    _set_headings(sheet)

    days_in_curr_month = _get_days_in_curr_month()
    hours_in_curr_month = days_in_curr_month * 24
    error_style = xlwt.easyxf("pattern: pattern solid, fore_colour red")
    name_style = xlwt.easyxf("pattern: pattern solid, fore_colour green")
    calc_style = xlwt.easyxf("pattern: pattern solid, fore_colour blue")

    i = 1
    for attendance in attendances:
        sheet.write(i, 0, attendance.name, name_style)
        sheet.write(i, 1, attendance.present)
        sheet.write(i, 2, attendance.absent)
        sheet.write(i, 3, attendance.leaves)
        sheet.write(i, 4, attendance.off_present)
        sheet.write(i, 5, attendance.over_time)
        sheet.write(i, 6, attendance.late_by)
        sheet.write(i, 7, attendance.early_by)
        salary = _get_salary_by(attendance.name)
        if salary == 0:
            sheet.write(i, 8, salary, error_style)
        else:
            sheet.write(i, 8, salary)
        cell_index = i + 1
        sheet.write(i, 9,
                    Formula("((B{index}*(I{index}/{days})) + "
                            "(E{index}*(I{index}/{days})) + "
                            "(F{index}*(I{index}/{hours}))) - "
                            "(C{index}*(I{index}/{days})) - "
                            "(D{index}*(I{index}/{days})) - "
                            "(G{index}*(I{index}/{hours})) - "
                            "(H{index}*(I{index}/{hours}))"
                            .format(index=cell_index,
                                    days=days_in_curr_month,
                                    hours=hours_in_curr_month)), calc_style)
        i += 1

    workbook.save(_get_path_to_exe(path))


def _get_salary_by(emp_name):
    """get salary by employee name"""

    employees = list(get_salaries()["employees"])
    employee = list(filter(lambda element: element["name"] == emp_name, employees))
    if not employee:
        return 0
    return employee[0]["salary"]


# pylint: disable=W0612
# reason: require weekday to unpack tuple
def _get_days_in_curr_month():
    """gets days in curr month"""

    year = date.today().year
    month = date.today().month
    (weekday, num_of_days) = monthrange(year, month)
    return num_of_days


def _set_headings(sheet):
    """sets headings in workbook sheet"""

    heading_style = xlwt.easyxf("pattern: pattern solid, fore_colour yellow")
    sheet.write(0, 0, "Name", heading_style)
    sheet.write(0, 1, "Present Days", heading_style)
    sheet.write(0, 2, "Absent Days", heading_style)
    sheet.write(0, 3, "Leaves", heading_style)
    sheet.write(0, 4, "Off Days Present", heading_style)
    sheet.write(0, 5, "Overtime", heading_style)
    sheet.write(0, 6, "Late By", heading_style)
    sheet.write(0, 7, "Early By", heading_style)
    sheet.write(0, 8, "Salary", heading_style)
    sheet.write(0, 9, "Calculated Salary", heading_style)


def _get_path_to_exe(path):
    """get file name from path"""

    file_path_arr = path.split("/")
    file_name = file_path_arr[len(file_path_arr) - 1]
    file_name = file_name + "- CALCULATED.xls"

    if hasattr(sys, "frozen"):
        return os.path.join(PATH_TO_EXE, file_name)

    return file_name
