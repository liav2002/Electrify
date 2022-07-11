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

    sqlHandler = create_connection(db_file)

    sqlHandler.commit()
    sqlHandler.close()
    return True


def add_user(db_file, id, username, email, password, phone, first_name, last_name):
    """ Add new User to Users table """

    sqlHandler = create_connection(db_file)

    sqlHandler.commit()
    sqlHandler.close()
    return True


def add_credit(db_file, user_id, c_number, cvv, validity):
    """ Add new Credit to Credit table """

    sqlHandler = create_connection(db_file)

    sqlHandler.commit()
    sqlHandler.close()
    return True


def add_battery(db_file, id, user_id, capacity, consumption):
    """ Add new Battery to Batteries table """

    sqlHandler = create_connection(db_file)

    sqlHandler.commit()
    sqlHandler.close()
    return True
