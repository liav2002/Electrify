from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from sql import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '584107ac33a499cb87847a6265f3bc1be'
app.config['DATABASE'] = 'ElectrifyDataBase.sqlite'

global isLoggedIn
isLoggedIn = False


@app.route("/")
def home():
    return render_template('home.html', isLoggedIn=isLoggedIn)


@app.route("/system")
def system():
    return render_template('system.html', isLoggedIn=isLoggedIn)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if add_user(app.config['DATABASE'], form.id.data, form.username.data, form.email.data, form.password.data,
                    form.phone.data, form.first_name.data, form.last_name.data) and add_credit(app.config['DATABASE'],
                                                                                               form.id.data,
                                                                                               form.c_number.data,
                                                                                               form.cvv.data,
                                                                                               form.c_month.data,
                                                                                               form.c_year.data):
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Failed to create account.', 'danger')
    return render_template('Register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if check_login_fields(app.config['DATABASE'], form.email.data, form.password.data):
            flash('You have been logged in!', 'success')
            global isLoggedIn
            isLoggedIn = True
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    flash('You have been logged out', 'success')

    global isLoggedIn
    isLoggedIn = False

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
