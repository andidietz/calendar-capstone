from flask import session
from models import db, Staff, Appointment
from secret_keys import TEAMUP_API_KEY
import requests 

TEAMUP_BASE_URL = 'https://api.teamup.com'
CALENDAR_KEY = 'zbypta'
SUBCALENDAR_KEYS = {
    'second_appt': 9387377,
    'annual_review': 9382928,
    'requested_appt_or_policy_delivery': 9381286,
    'workshop': 9381285
}

def get_users_staff_id():
    return Staff.query.filter_by(full_name=session['user']).one()

def serialize_search_results(appt):
    return {
        'teamup_id': appt.teamup_id,
        'category': appt.category,
        'start_time': appt.start_time,
        'end_time': appt.end_time,
        'title': appt.title,
        'note': appt.note
    }
    
def format_teamup_request(appt):
    return {
        'title': appt.title,
        'start_dt': appt.start_time,
        'end_dt': appt.end_time,
        'subcalendar_ids': appt.category,
        'notes': appt.note,
        'Teamup-Token': TEAMUP_API_KEY
    }

def create_appt_with_teamup_api(appt):
    formatted_params = format_teamup_request(appt)
    resp = requests.post(f'{TEAMUP_BASE_URL}/{CALENDAR_KEY}/events', params=formatted_params)
    return resp

def update_appt_with_teamup_api(appt):
    formatted_params = format_teamup_request(appt)
    resp = requests.put(f'{TEAMUP_BASE_URL}/{CALENDAR_KEY}/events/{appt.teamup_id})', params={formatted_params})
    
    return resp

def update_or_create_appt_in_db(form):
        title = form.title.data
        start_time = form.start_time.data,
        end_time = form.end_time.data,
        appt_type = form.appt_type.data
        note = form.note.data
        
        staff = Staff.get_users_staff_id(session['user'])
    
        appt = Appointment(start_time=start_time, end_time=end_time, title=title, type_id=appt_type, note=note, staff_id=staff.id)
        cat = [ appt.append(cat) for cat in form.categories.data]
        
        db.session.add(appt)
        db.session.commit()

        return appt