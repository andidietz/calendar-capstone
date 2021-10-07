from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.fields.html5 import DateField, DateTimeLocalField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('email')
    password = PasswordField('password')

class ScheduleForm(FlaskForm):
    title = StringField('name')
    start_time = DateTimeLocalField('Start Date and Time', format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField('End Date and Time', format='%Y-%m-%dT%H:%M')
    categories = MultiCheckboxField('category', coerce=int)
    appt_type = SelectField('appt type', choices=[(1, 'in person'), (2, 'phone'), (3, 'zoom')], coerce=int)
    note = TextAreaField('note')

class NotesForm(FlaskForm):
    note = TextAreaField('note')