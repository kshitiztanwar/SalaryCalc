"""attendance of employees"""

import re
import xlrd

from salary_calc.app_constants import ROW_DIFF_FOR_EMP_NAME, ROW_DIFF_FOR_ATTEN_STATS, \
    COL_FOR_ATTEN_STATS, DAY_STATS_PATTERN, DURATION_STAT_PATTERN


# pylint: disable=R0902, R0903
# reason: require many instance attributes and few public methods
class Attendance:
    """object to store attendance of employee"""

    # pylint: disable=R0913
    # reason: require many arguments
    def __init__(self, name, present, absent, leaves, off_present, over_time, late_by, early_by):
        self.name = name
        self.present = present
        self.absent = absent
        self.leaves = leaves
        self.off_present = off_present
        self.over_time = over_time
        self.late_by = late_by
        self.early_by = early_by


class AttendanceManager:
    """object to parse and store attendance of employees"""

    def __init__(self, path):
        self.path = path
        self.attendances = []
        self._parse_attendance_sheet()

    def _parse_attendance_sheet(self):
        """parse attendance sheet and append within object"""

        workbook = xlrd.open_workbook(self.path)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows
        cols = sheet.ncols

        for row in range(rows):
            for col in range(cols):
                cell = str(sheet.cell(row, col).value)
                if "Employee Name" in cell:
                    name = str(sheet.cell(row, col + ROW_DIFF_FOR_EMP_NAME).value)
                    attendance_stats = \
                        str(sheet.cell(row + ROW_DIFF_FOR_ATTEN_STATS, COL_FOR_ATTEN_STATS).value)
                    attendance = self._create_emp_attendance(name.strip(), attendance_stats)
                    self.attendances.append(attendance)

    def _create_emp_attendance(self, name, attendance_stats):
        """creates attendance object from name and attendance stats"""

        attendance_stats = attendance_stats.split("Total Duration")
        day_stats = re.findall(DAY_STATS_PATTERN, attendance_stats[0])
        duration_stats = re.findall(DURATION_STAT_PATTERN, attendance_stats[1])
        present = day_stats[0]
        absent = day_stats[1]
        leaves = day_stats[2]
        off_present = day_stats[3]
        over_time = self._convert_to_hours(duration_stats[1])
        late_by = self._convert_to_hours(duration_stats[2])
        early_by = self._convert_to_hours(duration_stats[3])

        return Attendance(name, present, absent, leaves, off_present, over_time, late_by, early_by)

    # pylint: disable=R0201
    # reason: require method here for clarity
    def _convert_to_hours(self, time):
        """converts hh:mm to hours"""
        time = time.replace(";", ":")  # handle error cases

        if time == ":":
            return 0

        time = time.split(":")
        return float(time[0]) + (float(time[1])/60)
