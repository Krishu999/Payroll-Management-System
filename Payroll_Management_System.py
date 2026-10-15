import mysql.connector as sqltor
import datetime
from tabulate import tabulate

db = input("Enter the name of your database : ")

mydb = sqltor.connect(host='localhost', user='root', password='yourpassword')
mycursor = mydb.cursor()

sql = "create database if not exists %s" % (db,)
mycursor.execute(sql)
print("Database created successfully... ")

mycursor = mydb.cursor()
mycursor.execute("Use " + db)

TableName = input("Name of table to be created : ")

query = "create table if not exists " + TableName + " (\
    empno int primary key,\
    name varchar(15) not null,\
    job varchar(15),\
    BasicSalary int,\
    DA float,\
    HRA float,\
    Tax float,\
    GrossSalary float,\
    NetSalary float)"
mycursor.execute(query)
print('Table ' + TableName + ' created successfully...')

while True:
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
    print('Enter Choice : ', end='')
    choice = int(input())

    if choice == 1:
        try:
            print('Enter employee information...')
    
            mempno = int(input('Enter employee no. : '))
            mname = input('Enter employee name : ')
            mjob = input('Enter employee job : ')
            mbasic = float(input('Enter basic salary : '))

            if mjob.upper() == 'OFFICER':
                mda = mbasic * 0.5
                mhra = mbasic * 0.35
                mtax = mbasic * 0.15
            elif mjob.upper() == 'MANAGER':
                mda = mbasic * 0.45
                mhra = mbasic * 0.30
                mtax = mbasic * 0.1
            else:
                mda = mbasic * 0.45
                mhra = mbasic * 0.30
                mtax = mbasic * 0.1

            mgross = mbasic + mda + mhra
            mnet = mgross - mtax

            rec = (mempno, mname, mjob, mbasic, mda, mhra, mtax, mgross, mnet)
            query = "insert into " + TableName + " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(query, rec)
            mydb.commit()
            print('Record added successfully...')

        except Exception as e:
            print('Something went wrong...', e)

    elif choice == 2:
        try:
            query = 'select * from ' + TableName
            mycursor.execute(query)
            print(tabulate(mycursor,
                           headers=['EmpNo', 'EmpName', 'Job', 'Basic Salary', 'DA',
                                    'HRA', 'Tax', 'Gross Salary', 'Net Salary'],
                           tablefmt='fancy_grid'))

        except Exception as e:
            print('Something went wrong', e)

    elif choice == 3:
        try:
            en = input('Enter employee no. of the record to be displayed : ')
            query = 'select * from ' + TableName + ' where empno= ' + en
            mycursor.execute(query)
            myrecord = mycursor.fetchone()
            print('\n\nRecord of Employee No. ' + en + ' : ')
            print(tabulate([myrecord],
                           headers=['EmpNo', 'EmpName', 'Job', 'Basic Salary', 'DA',
                                    'HRA', 'Tax', 'Gross Salary', 'Net Salary'],
                           tablefmt='fancy_grid'))
            
            c = mycursor.rowcount
            if c == -1:
                print('Nothing to display')

        except Exception as e:
            print('Something went wrong', e)

    elif choice == 4:
        try:
            ch = input('Do you want to delete records of all employees? (y/n) ')
            if ch.upper() == 'Y':
                mycursor.execute('delete from ' + TableName)
                mydb.commit()
                print('All the records are deleted...')

        except Exception as e:
            print('Something went wrong', e)

    elif choice == 5:
        try:
            en = input('Enter employee no. of the record to be deleted: ')
            query = 'delete from ' + TableName + ' where empno = ' + en
            mycursor.execute(query)
            mydb.commit()
            c = mycursor.rowcount
            if c > 0:
                print('Deletion done')
            else:
                print('Employee no', en, 'not found')
        except Exception as e:
            print('Something went wrong', e)

    elif choice == 6:
        try:
            en = input('Enter employee no. of the record to be modified: ')
            query = 'select * from ' + TableName + ' where empno = ' + en
            mycursor.execute(query)
            myrecord = mycursor.fetchone()
            c = mycursor.rowcount
            if c == -1:
                print('Empno ' + en + ' does not exist')
            else:
                mname = myrecord[1]
                mjob = myrecord[2]
                mbasic = myrecord[3]
                print('empno : ', myrecord[0])
                print('name : ', myrecord[1])
                print('job : ', myrecord[2])
                print('basic : ', myrecord[3])
                print('da : ', myrecord[4])
                print('hra : ', myrecord[5])
                print('tax : ', myrecord[6])
                print('gross : ', myrecord[7])
                print('net : ', myrecord[8])
                print('-' * 90)

                print('Type value to modify below or just press enter for no change')

                x = input('Enter name : ')
                if len(x) > 0:
                    mname = x

                x = input('Enter job : ')
                if len(x) > 0:
                    mjob = x

                x = input('Enter basic salary : ')
                if len(x) > 0:
                    mbasic = float(x)

                query = "update " + TableName + " set name = '" + mname + "', job = '" + mjob + "', BasicSalary = '" + str(mbasic) + "' where empno = " + en
                mycursor.execute(query)
                mydb.commit()
                print('Record modified')

        except Exception as e:
            print('Something went wrong', e)

    elif choice == 7:
        try:
            query = 'select * from ' + TableName
            mycursor.execute(query)
            myrecords = mycursor.fetchall()

            print('\n\n\n')
            print('*' * 90)

            now = datetime.datetime.now()
            print("Current Date and Time : ", end='')
            print(now.strftime("%Y-%m-%d %H:%M:%S"))

            print()
            print(tabulate(myrecords,
                           headers=['EmpNo', 'Name', 'Job', 'Basic Salary', 'DA',
                                    'HRA', 'Tax', 'Gross Salary', 'Net Salary'],
                           tablefmt='fancy_grid'))

        except Exception as e:
            print('Something went wrong', e)

    elif choice == 8:
        try:
            query = 'select * from ' + TableName
            mycursor.execute(query)

            now = datetime.datetime.now()
            print('\n\n\n\t\tSALARY SLIP\n')
            print("Current Date and Time : ", end='')
            print(now.strftime("%Y-%m-%d %H:%M:%S"))

            print()
            myrecords = mycursor.fetchall()
            print(tabulate(myrecords,
                           headers=['EmpNo', 'EmpName', 'Job', 'Basic Salary', 'DA',
                                    'HRA', 'Tax', 'Gross Salary', 'Net Salary'],
                           tablefmt='fancy_grid'))
        
        except Exception as e:
            print('Something went wrong', e)

    elif choice == 9:
        try:
            en = input("Enter employee number whose pay slip you want to receive: ")

            query = "select * from " + TableName + " where Empno = " + en
            mycursor.execute(query)

            now = datetime.datetime.now()

            print("\n\n\n\t\tSALARY SLIP\n")
            print("Current Date and Time : ", end="")
            print(now.strftime("%Y-%m-%d %H:%M:%S"))

            print()

            myrecords = mycursor.fetchall()
            print(tabulate(myrecords,
                           headers=['EmpNo', 'EmpName', 'Job', 'Basic Salary', 'DA',
                                    'HRA', 'Tax', 'Gross Salary', 'Net Salary'],
                           tablefmt='fancy_grid'))

        except Exception as e:
            print("Something went wrong", e)

    elif choice == 10:
        break

    else:
        print("Wrong choice...")
