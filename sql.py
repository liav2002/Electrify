import sqlite3
from sqlite3 import Error

db_file = 'ElectrifyDataBase.sqlite'


def create_connection():
    """ create a database connection to a SQLite database """

    try:
        sqlHandler = sqlite3.connect(db_file)
        return sqlHandler
    except Error as e:
        print("ERROR:create_connection: " + str(e))


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


def add_user(id, username, email, password, phone, first_name, last_name, address, plan):
    """ Add new User to Users table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Users (ID, Username, Email, Password, Phone, FirstName, LastName, Address, Plan) " \
                f"VALUES ({id}, '{username}', '{email}', '{password}', '{phone}', '{first_name}', '{last_name}', " \
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


def add_battery(id, user_id, capacity, consumption):
    """ Add new Battery to Batteries table """

    status = True

    try:
        sqlHandler = create_connection()

        query = f"INSERT INTO Batteries (ID, UserID, Capacity, Consumption)" \
                f"VALUES ({id}, {user_id}, {capacity}, {consumption});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print("ERROR:add_battery: " + str(e))
        status = False

    return status


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


def get_battery_capacity(user_id):
    try:
        sqlHandler = create_connection()
        query = f"SELECT Capacity FROM Batteries WHERE UserID={user_id};"
        cursor = sqlHandler.execute(query)
        rows = cursor.fetchall()

        if len(rows) != 0:
            return float(rows[0][0])
        else:
            return -1

    except Error as e:
        print("ERROR:get_battery_capacity: " + str(e))
        return -1


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
