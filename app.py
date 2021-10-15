from flask import Flask, render_template, request, flash, redirect, session
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension

from helper import create_appt_with_teamup_api, serialize_search_results, update_appt_with_teamup_api, update_or_create_appt_in_db
from forms import ScheduleForm, LoginForm, RegisterForm, NotesForm
from models import db, connect_db, Staff, Appointment, Category, Type
from datetime import datetime

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calendar'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "Here's a secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

###################################################
# Login, Logout, Register Routes

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html')
    return redirect('/users/login')


# TODO: De-nest the if statements
@app.route('/users/login', methods=['GET', 'POST'])
def login_user():
    if 'user' in session:
        return redirect('/schedule/add')

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        staff = Staff.authenticate(email, password)
        
        if staff:
            session['user'] = staff.full_name
            return redirect('/schedule/add')
        else:
            flash('Invalid email or password. Please try again.')
    return render_template('users/login.html', form=form) 


@app.route('/users/register', methods=['GET', 'post'])
def register_staff():

    if 'user' in session:
        return redirect('/schedule/add')
    
    form = RegisterForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data

        staff = Staff.register(full_name, email, password)
        db.session.add(staff)
        db.session.commit()

        session['user'] = staff.full_name
        
        return redirect('/schedule/add')
    return render_template('users/register.html', form=form) 

@app.route('/users/logout')
def logout():
    session.pop('user')
    return redirect('/users/login')

###################################################
# Schdeule Routes

# ERROR HERE: No Caught error, it completes its POST route and adds it to the db, 
# but it does not send the POST request to teamup API
@app.route('/schedule/add', methods=['GET', 'POST'])
def show_and_handle_schedule_form():
    """ GET: serve schedule form, reschedule form, and calendar 
   
    POST: handle the scheduling form
    """
    if 'user' not in session:
        flash('Must be logged in')
        return redirect('/login')

    form = ScheduleForm()

    categories = [(cat.id, cat.category) for cat in Category.query.all()]
    form.categories.choices = categories

    if form.validate_on_submit():
        appt = update_or_create_appt_in_db(form)
        flash('Appt Saved')

        try:
            saved_appt = create_appt_with_teamup_api(appt)
        except:
            print('Appt error')
    
        # return redirect(f'/notes/{appt.id}')
        return redirect('/schedule/add')

    return render_template('schedule/add.html', form=form)


##########################################################
# Note Routes
@app.route('/notes/<int:appt_id>', methods=['GET', 'POST'])
def show_and_handle_note_form(appt_id):
    """ GET: serve notes form and appt save success message
   
    POST: handle the notes form
    """
    if 'user' not in session:
        flash('Must be logged in')
        return redirect('/users/login')
 
    appt = Appointment.query.get_or_404(appt_id)
    form = NotesForm(obj=appt)

    if form.validate_on_submit():
        appt = update_or_create_appt_in_db(form)
        saved_apt = create_appt_with_teamup_api(appt)

        flash('Note Saved to Appointment')
        return redirect(f'/notes/{appt.id}', appt=appt, form=form)

    return render_template(f'/notes/{appt.id}', form=form)


############################################################
# Reschedule Routes

@app.route('/reschudule/search')
def serve_search_page():
    return render_template('reschedule/search.html')

@app.route('/<int:appt_id>/reschedule', methods=['GET','POST'])
def reschedule(appt_id):

    appt = Appointment.query.get_or_404(appt_id)
    form = ScheduleForm(obj=appt)

    categories = [(cat.teamup_id, cat.category) for cat in Category.query.all()]
    form.categories.choices = categories

    if form.validate_on_submit():
        appt = update_or_create_appt_in_db(form)
        update_appt_with_teamup_api(appt)
        
        flash('Appt Saved')
        return redirect('/calendar')
    return render_template('reschedule/update.html', form=form, appt=appt)


############################################################
# API Routes

#  ERROR HERE: JS axios call to this route returns a 500 internal server error
@app.route('/api/reschedule/search', methods=['GET'])
def query_appt_on_database():

    search_query = request.args['q']
    appts = Appointment.query.filter(Appointment.title.like(f'%{search_query}%')).all()

    serialized = [serialize_search_results(appt) for appt in appts]
    return jsonify(appts=serialized)

@app.route('/api/schedule/search', methods=['GET'])
def query_appt_on_hubspot():

    search_query = request.args['q']

    # TODO: Query Hubspot for clients
    
    serialized = [serialize_search_results(appt) for appt in appts]
    return jsonify(appts=serialized)