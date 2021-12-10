from flask import Flask, render_template, request, flash, redirect, session
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os

import helper
from forms import ScheduleForm, LoginForm, RegisterForm, NotesForm
from models import Category, db, connect_db, Staff, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'JesTer2')
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

###################################################
# Login, Logout, Register Routes

@app.route('/')
def home():
    """If user is logged in: displays home page.

    If not, redirects to login page.
    """

    if 'user' in session:
        return render_template('home.html')
    return redirect('/users/login')


@app.route('/users/login', methods=['GET', 'POST'])
def login_user():
    """If logged in: Redirects to home page.

    If not, displays login form. On Validate, redirects to home.
    """ 
    if 'user' in session:
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        staff = Staff.authenticate(email, password)
        
        if staff:
            session['user'] = staff.full_name
            session['admin'] = staff.admin
            flash('Log in successful', 'alert alert-success')

            return redirect('/')
        else:
            flash('Invalid email or password. Please try again.', 'alert alert-danger')
    return render_template('users/login.html', form=form) 


@app.route('/users/register', methods=['GET', 'post'])
def register_staff():
    """Display register form. 
    
    On Validate, creates Staff instances, commits staff to db, and redirects to home.
    """ 

    if 'user' in session:
        return redirect('/schedule/add')
    
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            full_name = form.full_name.data
            email = form.email.data
            password = form.password.data
            admin = form.admin.data

            staff = Staff.register(full_name, email, password, admin)
            db.session.add(staff)
            db.session.commit()

            session['user'] = staff.full_name
            
            return redirect('/')
        except:
            flash('Username already in use', 'alert alert-danger')
            redirect('/users/register')
    return render_template('users/register.html', form=form) 

@app.route('/users/logout')
def logout():
    """Logout user out of session""" 
    session.pop('user')
    return redirect('/users/login')

###################################################
# Schdeule Routes

@app.route('/schedule/add', methods=['GET', 'POST'])
def show_and_handle_schedule_form():
    """ GET: serve schedule form and calendar.
   
    POST: create appt in db and sends POST request to Teamup API to create new calendar event.
    """
    if 'user' not in session:
        flash('Must be logged in', 'alert alert-danger')
        return redirect('/login')

    form = ScheduleForm()
    categories = [(cat.id, cat.category) for cat in Category.query.all()]
    form.category_id.choices = categories

    if form.validate_on_submit():
        if helper.validate_endtime(form):
            appt = helper.create_appt_in_db(form)
            helper.create_appt_with_teamup_api(appt)

            flash('Appt Saved', 'alert alert-success')
            return redirect(f'/notes/{appt.id}/update')
        else:
            flash('Invalid Endtime', 'alert alert-danger')
            redirect('/schedule/add')
    return render_template('schedule/add.html', form=form)


############################################################
# Reschedule Routes

@app.route('/reschedule/search')
def serve_search_page():
    """ GET: serve search page to search appointments by title"""

    if 'user' not in session:
        flash('Must be logged in', 'alert alert-danger')
        return redirect('/users/login')
    return render_template('reschedule/search.html')


@app.route('/<int:appt_id>/update', methods=['GET','POST'])
def reschedule(appt_id):
    """ GET: serve calendar and reschedule form populated by appt's current details.
   
    POST: update appointment in db and on Teamup through Teamup API.
    """
    if 'user' not in session:
        flash('Must be logged in', 'alert alert-danger')
        return redirect('/users/login')

    appt = Appointment.query.get_or_404(appt_id)

    form = ScheduleForm(obj=appt)
    categories = [(cat.id, cat.category) for cat in Category.query.all()]
    form.category_id.choices = categories

    if form.validate_on_submit():
        appt = helper.update_appt_in_db(form, appt)
        helper.update_appt_with_teamup_api(appt)
        
        flash('Appt Saved', 'alert alert-success')
        return redirect(f'/notes/{appt_id}/update')
    return render_template('reschedule/update.html', appt=appt, form=form)


##########################################################
# Note and Delete Routes

@app.route('/notes/<int:appt_id>/update', methods=['GET', 'POST'])
def show_and_handle_note_form(appt_id):
    """ GET: serve notes form and appt save success message. 
    Purpose: allow users to write notes after ending schedule appts calls with clients.
   
    POST: update notes value in db and on Teamup through Teamup API.
    """
    if 'user' not in session:
        flash('Must be logged in', 'alert alert-danger')
        return redirect('/users/login')
 
    appt = Appointment.query.get_or_404(appt_id)
    form = NotesForm(obj=appt)

    if form.validate_on_submit():
        helper.update_note_in_db(form, appt)
        helper.update_appt_with_teamup_api(appt)
        flash('Appointment Updated', 'alert alert-success')
        return redirect('/')
    return render_template('notes/update.html', form=form, appt=appt)


@app.route('/<int:appt_id>/delete', methods=['GET'])
def delete_appt(appt_id):
    """If Admin, delete appt from db and Teamup Site using Teamup API, and redirect to home.
    
    If Not Admin, flash message and redirect to home.
    """
    if not 'admin':
        flash('Appointment Cannot Be Deleted From Scheduler', 'alert alert-danger')
        return redirect('/')

    appt = Appointment.query.get_or_404(appt_id)
    helper.delete_appt_in_db(appt)
    helper.delete_appt_on_teamup(appt)

    flash('Appointment Successfully Deleted', 'alert alert-success')
    return redirect('/')


############################################################
# API Routes

@app.route('/api/reschedule/search', methods=['GET'])
def query_appt_on_database():
    """ Queries db to find appointment by id and returns jsonified appointments matching query string"""

    search_query = request.args['q']
    appts = Appointment.query.filter(Appointment.title.ilike(f'%{search_query}%')).all()
    serialized = [helper.serialize_search_results(appt) for appt in appts]
    if not appts:
        return jsonify({'msg':'not found'})
    else:
        serialized = [helper.serialize_search_results(appt) for appt in appts]
        return jsonify(appts=serialized)
