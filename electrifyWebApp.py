from flask import Flask, render_template, url_for, flash, redirect

from sql import add_user, add_credit, check_login_fields, get_user_id_by_email, get_battery_capacity
from battery import generate_battery
from forms import RegistrationForm, LoginForm
import Secure

app = Flask(__name__)
app.config['SECRET_KEY'] = '584107ac33a499cb87847a6265f3bc1be'

user_id = 0


@app.route("/")
def home():
    return render_template('home.html', isLoggedIn=user_id != 0)


@app.route("/system")
def system():
    if user_id != 0:
        return render_template('system.html', isLoggedIn=user_id != 0, battery=get_battery_capacity(user_id))

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

        # try add user to our database
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
