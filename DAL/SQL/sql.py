import sqlite3
from sqlite3 import Error
from datetime import datetime
import calendar
import os

# get db file path
DAL_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_file = os.path.join(DAL_path, "SQL", "ElectrifyDataBase.sqlite")


def create_connection():
    """ create a database connection to a SQLite database """

    try:
        sqlHandler = sqlite3.connect(db_file)
        return sqlHandler
    except Error as e:
        print("ERROR:create_connection: " + str(e))


###############################################################################################################
#                                    add to database functions:                                               #
###############################################################################################################


def add_user(Id, username, email, password, phone, first_name, last_name, address, plan):
    """ Add new User to Users table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Users (ID, Username, Email, Password, Phone, FirstName, LastName, Address, Plan) " \
                f"VALUES ({Id}, '{username}', '{email}', '{password}', '{phone}', '{first_name}', '{last_name}', " \
                f"'{address}', '{plan}'); "
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:add_user: " + str(e))
        status = False

    return status


def add_credit(user_id, name_on_card, c_number, cvv, c_month, c_year):
    """ Add new Credit to Credit table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Credits (UserID, Name_On_Card, C_Number, CVV, C_Month, C_Year)" \
                f"VALUES ({user_id}, '{name_on_card}','{c_number}', {cvv}, '{c_month}', {c_year});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:add_credit: " + str(e))
        status = False

    return status


def add_battery(Id, user_id, capacity, consumption):
    """ Add new Battery to Batteries table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Batteries (ID, UserID, Capacity, Consumption)" \
                f"VALUES ({Id}, {user_id}, {capacity}, {consumption});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:add_battery: " + str(e))
        status = False

    return status


def add_sample(Id, user_id, time, power, voltage):
    """ Add new Sample to Samples table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Samples (ID, UserID, Time, Power, Voltage)" \
                f"VALUES ({Id}, {user_id}, '{time}', {power}, {voltage});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:add_sample: " + str(e))
        status = False

    return status


###############################################################################################################
#                                       validate data functions:                                              #
###############################################################################################################


def check_login_fields(email, password):
    """ Checks whether the user is registered to the system and whether the password is correct """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Users WHERE Email = '{email}' AND Password = '{password}';"
        cursor = sqlHandler.execute(query)
        if cursor.fetchone()[0] != 1:
            status = False

        sqlHandler.commit()
        sqlHandler.close()

    except Exception as e:
        print("ERROR:check_login_fields: " + str(e))
        status = False

    return status


def is_userID_unique(user_id):
    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        result = cursor.fetchone()[0]

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:is_userID_unique: " + str(e))
        result = -1

    return result == 0


def is_username_unique(username):
    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Users WHERE Username='{username}';"
        cursor = sqlHandler.execute(query)
        result = cursor.fetchone()[0]

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:is_username_unique: " + str(e))
        result = -1

    return result == 0


def is_email_unique(email):
    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Users WHERE Email='{email}';"
        cursor = sqlHandler.execute(query)
        result = cursor.fetchone()[0]

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:is_username_unique: " + str(e))
        result = -1

    return result == 0


###############################################################################################################
#                                         getters functions:                                                  #
###############################################################################################################


def get_number_of_batteries():
    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Batteries;"
        cursor = sqlHandler.execute(query)
        result = cursor.fetchone()[0]

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:get_number_of_batteries: " + str(e))
        result = -1

    return result


def get_number_of_samples(user_id):
    try:
        sqlHandler = create_connection()

        query = f"SELECT COUNT(*) FROM Samples WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        result = cursor.fetchone()[0]

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:get_number_of_samples: " + str(e))
        result = -1

    return result


def get_user_id_by_email(email):
    try:
        sqlHandler = create_connection()
        query = f"SELECT ID FROM Users WHERE Email='{email}';"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return int(rows[0][0])
        else:
            return 0

    except Error as e:
        print("ERROR:get_user_id_by_email: " + str(e))
        return 0


def get_battery_id(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT ID FROM Batteries WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return int(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_battery_id: " + str(e))
        return -1


def get_battery_capacity(battery_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Capacity FROM Batteries WHERE ID={battery_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return float(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_battery_capacity: " + str(e))
        return -1


def get_battery_consumption(battery_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Consumption FROM Batteries WHERE ID={battery_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return float(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_battery_consumption: " + str(e))
        return -1


def get_username(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Username FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_username: " + str(e))
        return -1


def get_email(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Email FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_email: " + str(e))
        return -1


def get_password(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Password FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_password: " + str(e))
        return -1


def get_phone(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Phone FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_phone: " + str(e))
        return -1


def get_first_name(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT FirstName FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_first_name: " + str(e))
        return -1


def get_last_name(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT LastName FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_last_name: " + str(e))
        return -1


def get_address(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Address FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_address: " + str(e))
        return -1


def get_plan(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Plan FROM Users WHERE ID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_plan: " + str(e))
        return -1


def get_name_on_card(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Name_On_Card FROM Credits WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_name_on_card: " + str(e))
        return -1


def get_c_number(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT C_Number FROM Credits WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_c_number: " + str(e))
        return -1


def get_cvv(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT CVV FROM Credits WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return int(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_cvv: " + str(e))
        return -1


def get_c_month(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT C_Month FROM Credits WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return rows[0][0]
        else:
            return -1

    except Error as e:
        print("ERROR:get_c_month: " + str(e))
        return -1


def get_c_year(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT C_Year FROM Credits WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return int(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_c_year: " + str(e))
        return -1


def get_daily_consumption(user_id, date):
    try:
        sqlHandler = create_connection()
        consumption = {"Hour": "Power"}
        hours_filters = ['00:%', '01:%', '02:%', '03:%', '04:%', '05:%', '06:%', '07:%', '08:%', '09:%', '10:%', '11:%',
                         '12:%', '13:%', '14:%', '15:%', '16:%', '17:%', '18:%', '19:%', '20:%', '21:%', '22:%', '23:%']

        for f in hours_filters:
            query = f"SELECT SUM(Power) FROM Samples WHERE UserID={user_id} AND Time LIKE '{date + ' ' + f}';"
            cursor = sqlHandler.execute(query)
            rows = cursor.fetchall()
            if rows[0][0] is None:
                consumption[f[0:2] + ":00"] = 0
            else:
                consumption[f[0:2] + ":00"] = rows[0][0]

        return consumption

    except Error as e:
        print("ERROR:get_daily_consumption: " + str(e))
        return -1


def get_monthly_consumption(user_id):
    try:
        sqlHandler = create_connection()
        consumption = {"Hour": "Power"}

        currentMonth = datetime.today().month
        if currentMonth < 10:
            monthFilter = '%-0' + str(currentMonth) + '-%'
        else:
            monthFilter = '%-' + str(currentMonth) + '-%'

        filters = ['%-01', '%-02', '%-03', '%-04', '%-05', '%-06', '%-07', '%-08', '%-09', '%-10', '%-11', '%-12',
                   '%-13', '%-14', '%-15', '%-16', '%-17', '%-18', '%-19', '%-20', '%-21', '%-22', '%-23', '%-24',
                   '%-25', '%-26', '%-27', '%-28', '%-29', '%-30', '%-31']

        for dayFilter in filters:
            query = f"SELECT SUM(Power) FROM Samples WHERE UserID={user_id} AND date(Time) LIKE '{monthFilter}' AND date(Time) LIKE '{dayFilter}';"
            cursor = sqlHandler.execute(query)
            rows = cursor.fetchall()
            if rows[0][0] is None:
                consumption[dayFilter[2:]] = 0
            else:
                consumption[dayFilter[2:]] = rows[0][0]

        return consumption

    except Error as e:
        print("ERROR:get_monthly_consumption: " + str(e))
        return -1


def get_yearly_consumption(user_id):
    try:
        sqlHandler = create_connection()
        consumption = {"Day": "Power"}
        filters = ['%-01-%', '%-02-%', '%-03-%', '%-04-%', '%-05-%', '%-06-%',
                   '%-07-%', '%-08-%', '%-09-%', '%-10-%', '%-11-%', '%-12-%']

        for f in filters:
            query = f"SELECT SUM(Power) FROM Samples WHERE UserID={user_id} AND date(Time) LIKE '{f}';"
            cursor = sqlHandler.execute(query)
            rows = cursor.fetchall()
            if rows[0][0] is None:
                if f[2] != '0':
                    consumption[calendar.month_name[int(f[2:4])]] = 0
                else:
                    consumption[calendar.month_name[int(f[3])]] = 0
            else:
                if f[2] != '0':
                    consumption[calendar.month_name[int(f[2:4])]] = rows[0][0]
                else:
                    consumption[calendar.month_name[int(f[3])]] = rows[0][0]

        return consumption

    except Error as e:
        print("ERROR:get_yearly_consumption: " + str(e))
        return -1


###############################################################################################################
#                                         update functions:                                                   #
###############################################################################################################


def update_username(user_id, username):
    status = True

    try:
        sqlHandler = create_connection()
        query = f"Update Users SET Username='{username}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()
    except Error as e:
        print("ERROR:update_username: " + str(e))
        status = False

    return status


def update_email(user_id, email):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET Email='{email}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_email: " + str(e))
        status = False

    return status


def update_password(user_id, password):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET Password='{password}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_password: " + str(e))
        status = False

    return status


def update_phone(user_id, phone):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET Phone='{phone}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_phone: " + str(e))
        status = False

    return status


def update_first_name(user_id, first_name):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET FirstName='{first_name}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_first_name: " + str(e))
        status = False

    return status


def update_last_name(user_id, last_name):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET LastName='{last_name}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_last_name: " + str(e))
        status = False

    return status


def update_address(user_id, address):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET Address='{address}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_address: " + str(e))
        status = False

    return status


def update_plan(user_id, plan):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Users SET Plan='{plan}' WHERE ID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_plan: " + str(e))
        status = False

    return status


def update_name_on_card(user_id, name_on_card):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Credits SET Name_On_Card='{name_on_card}' WHERE UserID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_name_on_card: " + str(e))
        status = False

    return status


def update_c_number(user_id, c_number):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Credits SET C_Number='{c_number}' WHERE UserID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_c_number: " + str(e))
        status = False

    return status


def update_cvv(user_id, cvv):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Credits SET CVV={cvv} WHERE UserID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_cvv: " + str(e))
        status = False

    return status


def update_c_month(user_id, c_month):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Credits SET C_Month='{c_month}' WHERE UserID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_c_month: " + str(e))
        status = False

    return status


def update_c_year(user_id, c_year):
    status = True

    try:
        sqlHandler = create_connection()

        query = f"Update Credits SET C_Year={c_year} WHERE UserID={user_id};"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:update_c_year: " + str(e))
        status = False

    return status
