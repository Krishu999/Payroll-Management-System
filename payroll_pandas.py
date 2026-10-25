import os
import datetime
import pandas as pd
from tabulate import tabulate

COLUMNS = ['EmpNo', 'EmpName', 'Job', 'Basic Salary', 'DA',
           'HRA', 'Tax', 'Gross Salary', 'Net Salary']


# ---------------------------------------------------------------- file helpers
def load_data(filename):
    """Read the CSV into a DataFrame, or create an empty one if the file is new."""
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print('File loaded successfully...')
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(filename, index=False)
        print('New file created successfully...')
    return df


def save_data(df, filename):
    """Write the DataFrame back to the CSV file."""
    df.to_csv(filename, index=False)


# ------------------------------------------------------------- calculations
def calculate_salary(job, basic):
    """Return (da, hra, tax, gross, net) based on job and basic salary."""
    if job.upper() == 'OFFICER':
        da, hra, tax = basic * 0.5, basic * 0.35, basic * 0.15
    else:  # MANAGER and all other jobs
        da, hra, tax = basic * 0.45, basic * 0.30, basic * 0.1
    gross = basic + da + hra
    net = gross - tax
    return da, hra, tax, gross, net


def show_table(df):
    print(tabulate(df, headers=COLUMNS, tablefmt='fancy_grid', showindex=False))


def print_timestamp():
    now = datetime.datetime.now()
    print('Current Date and Time : ', now.strftime('%Y-%m-%d %H:%M:%S'))
    print()


# ---------------------------------------------------------------- operations
def add_employee(df, filename):
    try:
        print('Enter employee information...')
        empno = int(input('Enter employee no. : '))

        if (df['EmpNo'] == empno).any():
            print('Employee no', empno, 'already exists')
            return df

        name = input('Enter employee name : ')
        job = input('Enter employee job : ')
        basic = float(input('Enter basic salary : '))

        da, hra, tax, gross, net = calculate_salary(job, basic)
        new_row = pd.DataFrame([[empno, name, job, basic, da, hra, tax, gross, net]],
                               columns=COLUMNS)
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df, filename)
        print('Record added successfully...')
    except Exception as e:
        print('Something went wrong...', e)
    return df


def display_all(df):
    if df.empty:
        print('Nothing to display')
    else:
        show_table(df)


def display_one(df):
    try:
        empno = int(input('Enter employee no. of the record to be displayed : '))
        record = df[df['EmpNo'] == empno]
        if record.empty:
            print('Nothing to display')
        else:
            print('\n\nRecord of Employee No. ' + str(empno) + ' : ')
            show_table(record)
    except Exception as e:
        print('Something went wrong', e)


def delete_all(df, filename):
    try:
        ch = input('Do you want to delete records of all employees? (y/n) ')
        if ch.upper() == 'Y':
            df = pd.DataFrame(columns=COLUMNS)
            save_data(df, filename)
            print('All the records are deleted...')
    except Exception as e:
        print('Something went wrong', e)
    return df


def delete_one(df, filename):
    try:
        empno = int(input('Enter employee no. of the record to be deleted: '))
        mask = df['EmpNo'] == empno
        if mask.any():
            df = df[~mask].reset_index(drop=True)
            save_data(df, filename)
            print('Deletion done')
        else:
            print('Employee no', empno, 'not found')
    except Exception as e:
        print('Something went wrong', e)
    return df


def modify_record(df, filename):
    try:
        empno = int(input('Enter employee no. of the record to be modified: '))
        mask = df['EmpNo'] == empno
        if not mask.any():
            print('Empno ' + str(empno) + ' does not exist')
            return df

        idx = df.index[mask][0]
        row = df.loc[idx]

        print('empno : ', row['EmpNo'])
        print('name : ', row['EmpName'])
        print('job : ', row['Job'])
        print('basic : ', row['Basic Salary'])
        print('da : ', row['DA'])
        print('hra : ', row['HRA'])
        print('tax : ', row['Tax'])
        print('gross : ', row['Gross Salary'])
        print('net : ', row['Net Salary'])
        print('-' * 90)

        print('Type value to modify below or just press enter for no change')
        name, job, basic = row['EmpName'], row['Job'], float(row['Basic Salary'])

        x = input('Enter name : ')
        if x:
            name = x
        x = input('Enter job : ')
        if x:
            job = x
        x = input('Enter basic salary : ')
        if x:
            basic = float(x)

        # recompute dependent columns so the record stays consistent
        da, hra, tax, gross, net = calculate_salary(job, basic)
        df.loc[idx, COLUMNS[1:]] = [name, job, basic, da, hra, tax, gross, net]
        save_data(df, filename)
        print('Record modified')
    except Exception as e:
        print('Something went wrong', e)
    return df


def display_payroll(df):
    print('\n\n\n')
    print('*' * 90)
    print_timestamp()
    display_all(df)


def salary_slip_all(df):
    print('\n\n\n\t\tSALARY SLIP\n')
    print_timestamp()
    display_all(df)


def salary_slip_one(df):
    try:
        empno = int(input('Enter employee number whose pay slip you want to receive: '))
        record = df[df['EmpNo'] == empno]
        print('\n\n\n\t\tSALARY SLIP\n')
        print_timestamp()
        if record.empty:
            print('Employee no', empno, 'not found')
        else:
            show_table(record)
    except Exception as e:
        print('Something went wrong', e)


# ---------------------------------------------------------------------- menu
def print_menu():
    print('\n\n\n')
    print('*' * 90)
    print('\t\t\tMAIN MENU')
    print('*' * 90)
    print('\t\t1. Adding employee records')
    print('\t\t2. For displaying records of ALL the employees')
    print('\t\t3. For displaying record of a particular employee')
    print('\t\t4. For deleting records of ALL the employees')
    print('\t\t5. For deleting record of a particular employee')
    print('\t\t6. For modification in a record')
    print('\t\t7. For displaying payroll')
    print('\t\t8. For displaying salary slip for all the employees')
    print('\t\t9. For displaying salary slip for a particular employee')
    print('\t\t10. For exit')
    print('\n\n\n')


def main():
    filename = input('Enter the CSV file name (e.g. employees.csv) : ').strip()
    if not filename.lower().endswith('.csv'):
        filename += '.csv'
    df = load_data(filename)

    while True:
        print_menu()
        try:
            choice = int(input('Enter Choice : '))
        except ValueError:
            print('Please enter a number...')
            continue

        if choice == 1:
            df = add_employee(df, filename)
        elif choice == 2:
            display_all(df)
        elif choice == 3:
            display_one(df)
        elif choice == 4:
            df = delete_all(df, filename)
        elif choice == 5:
            df = delete_one(df, filename)
        elif choice == 6:
            df = modify_record(df, filename)
        elif choice == 7:
            display_payroll(df)
        elif choice == 8:
            salary_slip_all(df)
        elif choice == 9:
            salary_slip_one(df)
        elif choice == 10:
            break
        else:
            print('Wrong choice...')


if __name__ == '__main__':
    main()
