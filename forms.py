from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.fields.html5 import TimeField, DateField

class LoginForm(FlaskForm):
    email = StringField('email:')
    password = PasswordField('password:')

class RegisterForm(FlaskForm):
    full_name = StringField('full name')
    email = StringField('email')
    password = PasswordField('password')

class MultiCheckboxField(SelectMultipleField):
     widget = widgets.ListWidget(prefix_label=False)
     option_widget = widgets.CheckboxInput()

class ScheduleForm(FlaskForm):
    title = StringField('Name')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time')
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('End Time')
    category = SelectField('category', choices=[(1, 'second appt'), (2, 'annual review'), (3, 'requested appt or policy delivery'), (4, 'workshop'), (5, 'cancelled')], coerce=int)
    appt_type = SelectField('appt type', choices=[(1, 'in person'), (2, 'phone'), (3, 'zoom')], coerce=int)
    note = TextAreaField('note')

class NotesForm(FlaskForm):
    note = TextAreaField('note')