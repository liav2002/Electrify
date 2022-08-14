from sql import *

batteries_count = get_number_of_batteries()


def generate_battery(user_id):
    status = True

    global batteries_count
    if add_battery(batteries_count + 1, user_id, 100, 0):
        batteries_count += 1

    else:
        status = False

    return status
