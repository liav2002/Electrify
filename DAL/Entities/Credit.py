from DAL.SQL.sql import get_name_on_card, get_c_number, get_cvv, get_c_month, get_c_year
from DAL.SQL.sql import update_name_on_card, update_c_number, update_cvv, update_c_month, update_c_year


class Credit:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name_on_card = get_name_on_card(user_id)
        self.c_number = get_c_number(user_id)
        self.cvv = get_cvv(user_id)
        self.c_month = get_c_month(user_id)
        self.c_year = get_c_year(user_id)

    def update_name_on_card(self, new_name_on_card):
        update_name_on_card(self.user_id, new_name_on_card)
        self.name_on_card = new_name_on_card

    def update_c_number(self, new_c_number):
        update_c_number(self.user_id, new_c_number)
        self.c_number = new_c_number

    def update_cvv(self, new_cvv):
        update_cvv(self.user_id, new_cvv)
        self.cvv = new_cvv

    def update_c_month(self, new_c_month):
        update_c_month(self.user_id, new_c_month)
        self.c_month = new_c_month

    def update_c_year(self, new_c_year):
        update_c_year(self.user_id, new_c_year)
        self.c_year = new_c_year
