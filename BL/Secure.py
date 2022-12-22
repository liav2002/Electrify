from DAL import sql


def sqlInjection(value):
    black_list = ['&', '|', '~', '=', "DROP", "drop", "WHERE", "where", "ALTER", "alter", "UPDATE", "update", "OR",
                  "or", "AND", "and"]

    for char in str(value):
        if char in black_list:
            raise Exception("You really try it now ?!")


# register's input check

def check_user_id(user_id):
    try:  # convert it into integer
        val = int(user_id)
    except ValueError:
        raise Exception("User's id cannot contain characters and letters.")

    # check user's id length
    if len(str(user_id)) < 8 or len(str(user_id)) > 9:
        raise Exception("User's id length is invalid.")

    # before get into database, secure from sqlInjection
    sqlInjection(user_id)

    # Final, check if it is unique
    if not (sql.is_userID_unique(user_id)):
        raise Exception("User's id already registered in the system.")


def check_username(username):
    # before get into database, secure from sqlInjection
    sqlInjection(username)

    # Final, check if it is unique
    if not (sql.is_username_unique(username)):
        raise Exception("Username\talready\tregistered\tin\tthe\tsystem.")


def check_email(email, login):
    # before get into database, secure from sqlInjection
    sqlInjection(email)

    # Final, check if it is unique
    if not (sql.is_email_unique(email)) and not(login):
        raise Exception("Email already registered in the system.")


def check_password(password):
    # before get into database, secure from sqlInjection
    sqlInjection(password)

    # maybe it will be better to check the strong of the password


def check_phone(phone):
    # before get into database, secure from sqlInjection
    sqlInjection(phone)

    # maybe it will be better to check phone format


def check_first_name(first_name):
    # before get into database, secure from sqlInjection
    sqlInjection(first_name)


def check_last_name(last_name):
    # before get into database, secure from sqlInjection
    sqlInjection(last_name)


def check_address(address):
    # before get into database, secure from sqlInjection
    sqlInjection(address)

    # maybe it will be better to check if it's a real address


def check_name_on_card(name):
    # before get into database, secure from sqlInjection
    sqlInjection(name)


def check_c_number(c_number):
    # before get into database, secure from sqlInjection
    sqlInjection(c_number)

    # maybe it will be better to check the number format


def check_cvv(cvv):
    try:  # convert it into integer
        val = int(cvv)
    except ValueError:
        raise Exception("cvv cannot contain characters and letters.")

    # before get into database, secure from sqlInjection
    sqlInjection(cvv)
