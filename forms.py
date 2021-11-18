from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, PasswordField, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import TimeField, DateField

class LoginForm(FlaskForm):
    email = StringField('Email:')
    password = PasswordField('Password:')

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email')
    password = PasswordField('Password')
    admin = BooleanField('Admin')

class MultiCheckboxField(SelectMultipleField):
     widget = widgets.ListWidget(prefix_label=False)
     option_widget = widgets.CheckboxInput()

class ScheduleForm(FlaskForm):
    title = StringField('Title')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time')
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('End Time')
    category_id = SelectField('Category', coerce=int)
    type_id = SelectField('Appt type', choices=[(1, 'in person'), (2, 'phone'), (3, 'zoom')], coerce=int)
    note = TextAreaField('Note')

class NotesForm(FlaskForm):
    note = TextAreaField('Edit note section (optional). Save edited note or Click next to return to Home')