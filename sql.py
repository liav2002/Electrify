import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """

    try:
        sqlHandler = sqlite3.connect(db_file)
        return sqlHandler
    except Error as e:
        print(e)


def check_login_fields(db_file, email, password):
    """ Checks whether the user is registered to the system and whether the password is correct """

    status = True

    try:
        sqlHandler = create_connection(db_file)

        query = f"SELECT COUNT(*) FROM Users WHERE Email = '{email}' AND Password = '{password}';"
        cursor = sqlHandler.execute(query)
        if cursor.fetchone()[0] != 1:
            status = False

        sqlHandler.commit()
        sqlHandler.close()

    except Exception as e:
        print(e)
        status = False

    return status


def add_user(db_file, id, username, email, password, phone, first_name, last_name):
    """ Add new User to Users table """

    status = True

    try:
        sqlHandler = create_connection(db_file)

        query = f"INSERT INTO Users (ID, Username, Email, Password, Phone, FirstName, LastName) " \
                f"VALUES ({id}, '{username}', '{email}', '{password}', '{phone}', '{first_name}', '{last_name}');"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print(e)
        status = False

    return status


def add_credit(db_file, user_id, c_number, cvv, c_month, c_year):
    """ Add new Credit to Credit table """

    status = True

    try:
        sqlHandler = create_connection(db_file)

        query = f"INSERT INTO Credits (UserID, C_Number, CVV, C_Month, C_Year)" \
                f"VALUES ({user_id}, '{c_number}', {cvv}, '{c_month}', {c_year});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print(e)
        status = False

    return status


def add_battery(db_file, id, user_id, capacity, consumption):
    """ Add new Battery to Batteries table """

    status = True

    try:
        sqlHandler = create_connection(db_file)

        query = f"INSERT INTO Batteries (ID, UserID, Capacity, Consumption)" \
                f"VALUES ({id}, {user_id}, {capacity}, {consumption});"
        sqlHandler.execute(query)

        sqlHandler.commit()
        sqlHandler.close()

    except Error as e:
        print(e)
        status = False

    return status
