from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TelField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from backend.models import Rent_User

class RentReg(FlaskForm):
    name = StringField('Name', validators=[Length(min=3, max=30), DataRequired()])
    number = TelField('Phone Number', validators=[Length(min=10, max=15), DataRequired()])
    location = StringField('Location', validators=[Length(min=7), DataRequired()])
    aadhar = StringField('Aadhar Number', validators=[Length(min=12, max=12), DataRequired()])
    email_address = StringField('Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email_address(self, email_address_to_check):
        email_address = Rent_User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address.')


class RentLog(FlaskForm):
    email_address = StringField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')






class CustReg(FlaskForm):
    name = StringField('Name', validators=[Length(min=3, max=30), DataRequired()])
    number = TelField('Phone Number', validators=[Length(min=10, max=15), DataRequired()])
    location = StringField('Location', validators=[Length(min=7), DataRequired()])
    aadhar = StringField('Aadhar Number', validators=[Length(min=12, max=12), DataRequired()])
    email_address = StringField('Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email_address(self, email_address_to_check):
        email_address = Rent_User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address.')


class CustLog(FlaskForm):
    email_address = StringField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')