# python imports
import threading
import datetime

# setup project path directories
import sys
import os
projectDirPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DalPath = projectDirPath + "/DAL"
BLPath = projectDirPath + "/BL"
sysPath = []
sysPath.append(projectDirPath)
sysPath.append(DalPath)
sysPath.append(BLPath)
for place in sys.path:
    sysPath.append(place)
sys.path = sysPath

# web application imports
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AccountForm

from DAL.SQL.sql import add_user, add_credit, add_battery, \
    get_user_id_by_email, get_number_of_batteries, check_login_fields, get_battery_capacity, get_battery_id, \
    get_daily_consumption, get_current_measure, get_monthly_consumption, get_yearly_consumption
from DAL.Entities.User import User
from DAL.Entities.Credit import Credit
from DAL.Entities.Battery import Battery

from BL import Secure
from BL.os_detect import is_raspberrypi
from BL.INA219Handler import fill_samples

app = Flask(__name__)
app.config['SECRET_KEY'] = '584107ac33a499cb87847a6265f3bc1be'

RASPBERRY_PI = is_raspberrypi()
user_id = 0


@app.route("/")
def home():
    return render_template('home.html', isLoggedIn=user_id != 0)


@app.route("/system/get_battery_capacity", methods=['GET'])
def battery_capacity():
    return get_battery_capacity(get_battery_id(user_id))  # battery Xpath: /html/body/div[2]/div[1]/div[1]/div/div/div


@app.route("/system/get_summary_daily_consumption", methods=['GET'])
def summary_daily_consumption():
    return get_daily_consumption(user_id, datetime.datetime.now().strftime("%Y-%m-%d"))


@app.route("/system/get_current_measure", methods=['GET'])
def current_measure():
    return get_current_measure(user_id, str(datetime.datetime.now())[0:19])  # [0:19] --> for ignore ms


@app.route("/system/get_monthly_consumption", methods=['GET'])
def monthly_consumption():
    return get_monthly_consumption(user_id)


@app.route("/system/get_yearly_consumption", methods=['GET'])
def yearly_consumption():
    return get_yearly_consumption(user_id)


@app.route("/system", methods=['GET', 'POST'])
def system():
    if user_id != 0:
        form = AccountForm()
        user = User(user_id)
        credit = Credit(user_id)
        battery = Battery(user_id)

        # check if there is data to update
        if form.validate_on_submit():
            if form.username.data != user.username:
                try:  # check username input (security)
                    Secure.check_username(form.username.data)
                    user.update_username(form.username.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.username.errors += str(e)

            if form.email.data != user.email:
                try:  # check email input (security)
                    Secure.check_email(form.email.data, False)
                    user.update_email(form.email.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.email.errors += str(e)

            if form.password.data != user.password:
                try:  # check password input (security)
                    Secure.check_password(form.password.data)
                    user.update_password(form.password.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.password.errors += str(e)

            if form.phone.data != user.phone:
                try:  # check phone input (security)
                    Secure.check_phone(form.phone.data)
                    user.update_phone(form.phone.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.phone.errors += str(e)

            if form.first_name.data != user.first_name:
                try:  # check first name input (security)
                    Secure.check_first_name(form.first_name.data)
                    user.update_first_name(form.first_name.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.first_name.errors += str(e)

            if form.last_name.data != user.last_name:
                try:  # check last name input (security)
                    Secure.check_last_name(form.last_name.data)
                    user.update_last_name(form.last_name.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.last_name.errors += str(e)

            if form.address.data != user.address:
                try:  # check address input (security)
                    Secure.check_address(form.address.data)
                    user.update_address(form.address.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.address.errors += str(e)

            if form.plan.data != user.plan:
                # there is no input in this case, because we use select button -> no security problem.
                user.update_plan(form.plan.data)
                return redirect(url_for('system') + "#my-account")

            if form.name_on_card.data != credit.name_on_card:
                try:  # check name_on_card input (security)
                    Secure.check_name_on_card(form.name_on_card.data)
                    credit.update_name_on_card(form.name_on_card.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.name_on_card.errors += str(e)

            if form.c_number.data != credit.c_number:
                try:  # check c_number input (security)
                    Secure.check_c_number(form.c_number.data)
                    credit.update_c_number(form.c_number.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.c_number.errors += str(e)

            if int(form.cvv.data) != credit.cvv:
                try:  # check cvv input (security)
                    Secure.check_cvv(form.cvv.data)
                    credit.update_cvv(form.cvv.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.cvv.errors += str(e)

            if form.c_month.data != credit.c_month:
                # there is no input in this case, because we use select button -> no security problem.
                credit.update_c_month(form.c_month.data)
                return redirect(url_for('system') + "#my-account")

            if int(form.c_year.data) != credit.c_year:
                # there is no input in this case, because we use select button -> no security problem.
                credit.update_c_year(form.c_year.data)
                return redirect(url_for('system') + "#my-account")

        # TODO: update battery capacity and consumption real time.
        # TODO: update daily consumption real time.
        # TODO: fix bug: when we startup system window, the page show both of monthly and yearly consumption.
        #                (it should show only monthly consumption).

        return render_template('system.html', user=user, isLoggedIn=user_id != 0, battery=battery, credit=credit,
                               form=form, title="System")

    else:
        return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # secure user's input

        try:  # check user's id
            Secure.check_user_id(form.id.data)
        except Exception as e:
            form.id.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check username
            Secure.check_username(form.username.data)
        except Exception as e:
            form.username.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check email
            Secure.check_email(form.email.data, False)
        except Exception as e:
            form.email.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check password
            Secure.check_password(form.password.data)
        except Exception as e:
            form.password.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        if form.phone.data != '':  # phone it's not a must field
            try:  # check phone
                Secure.check_phone(form.phone.data)
            except Exception as e:
                form.phone.errors += str(e)
                return render_template('Register.html', title='Register', form=form)

        try:  # check first name
            Secure.check_first_name(form.first_name.data)
        except Exception as e:
            form.first_name.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check last name
            Secure.check_last_name(form.last_name.data)
        except Exception as e:
            form.last_name.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        if form.address.data != '':  # address it's not a must field
            try:  # check address
                Secure.check_address(form.address.data)
            except Exception as e:
                form.address.errors += str(e)
                return render_template('Register.html', title='Register', form=form)

        try:  # check name on card
            Secure.check_name_on_card(form.name_on_card.data)
        except Exception as e:
            form.name_on_card.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check c_number
            Secure.check_c_number(form.c_number.data)
        except Exception as e:
            form.c_number.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        try:  # check cvv
            Secure.check_cvv(form.cvv.data)
        except Exception as e:
            form.cvv.errors += str(e)
            return render_template('Register.html', title='Register', form=form)

        # try to add user to our database
        if add_user(form.id.data, form.username.data, form.email.data, form.password.data,
                    form.phone.data, form.first_name.data, form.last_name.data, form.address.data, form.plan.data) \
                and add_credit(form.id.data,
                               form.name_on_card.data,
                               form.c_number.data,
                               form.cvv.data,
                               form.c_month.data,
                               form.c_year.data) and generate_battery(form.id.data):
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('system'))
        else:
            flash(f'Failed to create account. Please contact our support team.', 'danger')

    return render_template('Register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # secure user's input

        try:  # check email
            Secure.check_email(form.email.data, True)
        except Exception as e:
            form.email.errors += str(e)
            return render_template('login.html', title='Login', form=form)

        try:  # check password
            Secure.check_password(form.password.data)
        except Exception as e:
            form.password.errors += str(e)
            return render_template('login.html', title='Login', form=form)

        if True:  # if check_login_fields(form.email.data, form.password.data):
            flash('You have been logged in!', 'success')
            global user_id
            user_id = 12345677  # user_id = get_user_id_by_email(form.email.data)

            if RASPBERRY_PI:
                # TODO: run background thread to use INA219 for measure Voltage, Power and update battery capacity
                print('Starting background task...')
                daemon = threading.Thread(target=fill_samples, args=(user_id,), daemon=True, name='Monitor')
                daemon.start()

            return redirect(url_for('system'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    flash('You have been logged out', 'success')

    global user_id
    user_id = 0

    return redirect(url_for('home'))


def generate_battery(uid):
    status = True

    batteries_count = get_number_of_batteries()

    if add_battery(batteries_count + 1, uid, 100, 20):
        batteries_count += 1

    else:
        status = False

    return status


if __name__ == '__main__':
    app.run(debug=True)
