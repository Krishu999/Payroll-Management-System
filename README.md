# Payroll Management System

A menu-driven command-line payroll manager written in Python. It uses **pandas** for data handling and stores employee records in a **CSV file**, so your data persists between runs.

## Features

- Add new employee records (duplicate employee numbers are rejected)
- Display all employees (summary view) or a single employee (full details)
- Modify an existing record (press Enter to keep a field unchanged)
- Delete a single employee or all employees
- View the complete payroll table with a timestamp
- Generate a formatted monthly salary slip for any employee
- Automatic CSV creation if the file doesn't exist yet

## Salary Calculation

DA, HRA and Tax are calculated as a percentage of Basic Salary, depending on the job title:

| Job     | DA  | HRA | Tax |
|---------|-----|-----|-----|
| Officer | 50% | 35% | 15% |
| Others  | 45% | 30% | 10% |

```
Gross Salary = Basic + DA + HRA
Net Salary   = Gross - Tax
```

The job title comparison is case-insensitive.

## Requirements

- Python 3.7+
- [pandas](https://pandas.pydata.org/)
- [tabulate](https://pypi.org/project/tabulate/)

## Installation

```bash
git clone https://github.com/Krishu999/Payroll-Management-System.git
pip install pandas tabulate
```

## Usage

```bash
python payroll_pandas.py
```

You'll first be asked for a CSV file name (e.g. `employees` or `employees.csv`). If the file exists it is loaded; otherwise a new one is created. Then choose from the main menu:

```
1. Adding employee records
2. For displaying records of ALL the employees
3. For displaying record of a particular employee
4. For deleting records of ALL the employees
5. For deleting record of a particular employee
6. For modification in a record
7. For displaying payroll
8. For displaying salary slip for a particular employee
9. For exit
```

## Project Members

| Name              | Roll Number |
|-------------------|-------------|
| Krishnav Agarwal  | 26BYB0145   |
| Dev Dagar         | 26BYB0175   |
| Akshat Swarup     | 26BYB0168   |
