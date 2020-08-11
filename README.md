# Salary Calculator

- This is an application to automatically track and calculate hourly salaries based on attendance sheets collected from ESSL Biometric Machines.
- The application provides an interface for managing salaries, along with features to calculate monthly salaries.
- Once calculated application returns an excel sheet with calculated salaries and embedded formulas for further customization in calculations.


- **Functionality**
    - Attach attendance excel sheet from ESSL Biometric Machine
    - Press 'Calculate & Save' button
    - Open fully customizable excel sheet with calculated salaries and formulas for further customization 


- **Steps to Build**
    - Create a virtual environment for Python
    - Install requirements.txt
    - Build using the command below
        - `pyinstaller --onefile --add-data='salary.json:.' --paths <PATH-TO-VIRTUAL-ENVIRONMENT>/venv/lib/python3.8/site-packages app.py`
