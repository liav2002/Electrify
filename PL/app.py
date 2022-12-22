from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AccountForm

from DAL.sql import *

from BL.battery import generate_battery
from BL import Secure
from BL.os_detect import is_raspberrypi

app = Flask(__name__)
app.config['SECRET_KEY'] = '584107ac33a499cb87847a6265f3bc1be'

RASPBERRY_PI = is_raspberrypi()
user_id = 0


@app.route("/")
def home():
    return render_template('home.html', isLoggedIn=user_id != 0)


@app.route("/system", methods=['GET', 'POST'])
def system():
    if user_id != 0:
        form = AccountForm()
        username = get_username(user_id)
        email = get_email(user_id)
        password = get_password(user_id)
        phone = get_phone(user_id)
        first_name = get_first_name(user_id)
        last_name = get_last_name(user_id)
        address = get_address(user_id)
        plan = get_plan(user_id)
        name_on_card = get_name_on_card(user_id)
        c_number = get_c_number(user_id)
        cvv = get_cvv(user_id)
        c_month = get_c_month(user_id)
        c_year = get_c_year(user_id)

        # check if there is data to update
        if form.validate_on_submit():
            if form.username.data != username:
                try:  # check username input (security)
                    Secure.check_username(form.username.data)
                    update_username(user_id, form.username.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.username.errors += str(e)

            if form.email.data != email:
                try:  # check email input (security)
                    Secure.check_email(form.email.data, False)
                    update_email(user_id, form.email.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.email.errors += str(e)

            if form.password.data != password:
                try:  # check password input (security)
                    Secure.check_password(form.password.data)
                    update_password(user_id, form.password.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.password.errors += str(e)

            if form.phone.data != phone:
                try:  # check phone input (security)
                    Secure.check_phone(form.phone.data)
                    update_phone(user_id, form.phone.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.phone.errors += str(e)

            if form.first_name.data != first_name:
                try:  # check first name input (security)
                    Secure.check_first_name(form.first_name.data)
                    update_first_name(user_id, form.first_name.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.first_name.errors += str(e)

            if form.last_name.data != last_name:
                try:  # check last name input (security)
                    Secure.check_last_name(form.last_name.data)
                    update_last_name(user_id, form.last_name.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.last_name.errors += str(e)

            if form.address.data != address:
                try:  # check address input (security)
                    Secure.check_address(form.address.data)
                    update_address(user_id, form.address.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.address.errors += str(e)

            if form.plan.data != plan:
                # there is no input in this case, because we use select button -> no security problem.
                update_plan(user_id, form.plan.data)
                return redirect(url_for('system') + "#my-account")

            if form.name_on_card.data != name_on_card:
                try:  # check name_on_card input (security)
                    Secure.check_name_on_card(form.name_on_card.data)
                    update_name_on_card(user_id, form.name_on_card.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.name_on_card.errors += str(e)

            if form.c_number.data != c_number:
                try:  # check c_number input (security)
                    Secure.check_c_number(form.c_number.data)
                    update_c_number(user_id, form.c_number.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.c_number.errors += str(e)

            if int(form.cvv.data) != cvv:
                try:  # check cvv input (security)
                    Secure.check_cvv(form.cvv.data)
                    update_cvv(user_id, form.cvv.data)
                    return redirect(url_for('system') + "#my-account")
                except Exception as e:
                    form.cvv.errors += str(e)

            if form.c_month.data != c_month:
                # there is no input in this case, because we use select button -> no security problem.
                update_c_month(user_id, form.c_month.data)
                return redirect(url_for('system') + "#my-account")

            if int(form.c_year.data) != c_year:
                # there is no input in this case, because we use select button -> no security problem.
                update_c_year(user_id, form.c_year.data)
                return redirect(url_for('system') + "#my-account")

        return render_template('system.html', isLoggedIn=user_id != 0, battery=get_battery_capacity(user_id),
                               username=username, email=email, password=password, phone=phone,
                               first_name=first_name,
                               last_name=last_name, address=address, plan=plan, name_on_card=name_on_card,
                               c_number=c_number, cvv=cvv, c_month=c_month, c_year=c_year,
                               daily_consumption=get_daily_consumption(user_id),
                               monthly_consumption=get_monthly_consumption(user_id),
                               yearly_consumption=get_yearly_consumption(user_id),
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

        if check_login_fields(form.email.data, form.password.data):
            flash('You have been logged in!', 'success')
            global user_id
            user_id = get_user_id_by_email(form.email.data)

            if RASPBERRY_PI:
                # TODO: run background thread to use INA219 for measure Voltage, Power and update battery capacity
                pass

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


if __name__ == '__main__':
    app.run(debug=True)
