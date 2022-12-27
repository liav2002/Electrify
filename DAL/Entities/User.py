from DAL.SQL.sql import get_username, get_email, get_password, get_phone, get_first_name, get_last_name, get_address, \
    get_plan

from DAL.SQL.sql import update_username, update_email, update_password, update_phone, update_first_name, \
    update_last_name, update_address, update_plan


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.username = get_username(user_id)
        self.email = get_email(user_id)
        self.password = get_password(user_id)
        self.phone = get_phone(user_id)
        self.first_name = get_first_name(user_id)
        self.last_name = get_last_name(user_id)
        self.address = get_address(user_id)
        self.plan = get_plan(user_id)

    def update_username(self, new_username):
        update_username(self.user_id, new_username)
        self.username = new_username

    def update_email(self, new_email):
        update_email(self.user_id, new_email)
        self.email = new_email

    def update_password(self, new_password):
        update_password(self.user_id, new_password)
        self.password = new_password

    def update_phone(self, new_phone):
        update_phone(self.user_id, new_phone)
        self.phone = new_phone

    def update_first_name(self, new_first_name):
        update_first_name(self.user_id, new_first_name)
        self.first_name = new_first_name

    def update_last_name(self, new_last_name):
        update_last_name(self.user_id, new_last_name)
        self.last_name = new_last_name

    def update_address(self, new_address):
        update_address(self.user_id, new_address)
        self.address = new_address

    def update_plan(self, new_plan):
        update_plan(self.user_id, new_plan)
        self.plan = new_plan
