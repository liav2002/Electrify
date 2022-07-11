from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, number_range


class RegistrationForm(FlaskForm):
    # User details
    id = IntegerField("User's ID",
                           validators=[DataRequired(), number_range(min=11111111, max=999999999)])
    first_name = StringField("First Name",
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField("Last Name",
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Credit details
    name_on_card = StringField('Name On Card',
                               validators=[DataRequired(), Length(min=2, max=20)])
    c_number = StringField('Credit Card Number',
                           validators=[DataRequired()])
    c_month = SelectField("Month", choices=["January", "February", "March", "April", "May", "June", "July", "August",
                                            "September", "October", "November", "December"],
                          validators=[DataRequired()])
    c_year = SelectField("Year",
                         choices=["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032"],
                         validators=[DataRequired()])
    cvv = IntegerField("CVV", validators=[DataRequired(), number_range(min=111, max=999)])


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
