from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, PasswordField, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(6)])
    admin = BooleanField('Admin')

class MultiCheckboxField(SelectMultipleField):
     widget = widgets.ListWidget(prefix_label=False)
     option_widget = widgets.CheckboxInput()

class ScheduleForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('End Time', validators=[InputRequired()])
    category_id = SelectField('Category', coerce=int)
    type_id = SelectField('Appt type', choices=[(1, 'in person'), (2, 'phone'), (3, 'zoom')], coerce=int)
    note = TextAreaField('Note')

class NotesForm(FlaskForm):
    note = TextAreaField('Edit note if needed and click save to continue.')