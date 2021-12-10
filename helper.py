from flask import session, jsonify
from models import Category, db, Staff, Appointment
import requests 
import json
import os

api_key = os.environ.get('TEAMUP_API_KEY')
calendar_id = os.environ.get('CALENDAR_ID')
TEAMUP_BASE_URL = 'https://api.teamup.com'


TEAMUP_GET_HEADERS = {
   'Teamup-Token': api_key,
}

TEAMUP_POST_HEADERS = {
    'Teamup-Token': api_key,
    'Content-type': 'application/json',
}

#############################################
# Helper Functions

def validate_value(field_name):
    if field_name:
        return field_name
    return None

def get_users_staff_id():
    """Query database and return current user from the Staff Model"""
    return Staff.query.filter_by(full_name=session['user']).one()

def serialize_search_results(appt):
    """Serialize database query to send the json data to the frontend"""
    
    start_date = appt.start_date.isoformat()
    start_time = appt.start_time.isoformat()
    end_date = appt.end_date.isoformat()
    end_time = appt.end_time.isoformat()

    return {
        "id": appt.id,
        "teamup_id": appt.teamup_id,
        "category": appt.category_id,
        "start_date": start_date,
        "start_time": start_time,
        "end_date": end_date,
        "end_time": end_time,
        "title": appt.title,
        "note": appt.note,
        "teamup_id": appt.teamup_id
    }

def validate_endtime(form):
    """Return None if appt's end time is before its start time"""
    if form.end_time.data < form.start_time.data:
        return None
    return 'Valid datetime'

#############################################
# Database

def update_note_in_db(form, appt):
    """Update appointment note in database"""

    appt.note = form.note.data
    db.session.commit()

    return form

def create_appt_in_db(form):
    """Create appointment in database"""

    title = form.title.data
    start_date = form.start_date.data
    start_time = form.start_time.data
    end_date = form.start_date.data
    end_time = form.end_time.data
    appt_type = form.type_id.data
    note = form.note.data
    
    staff = Staff.get_users_staff_id(session['user'])
    category = Category.query.get_or_404(form.category_id.data)

    appt = Appointment(category_id=category.id, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, title=title, type_id=appt_type, note=note, staff_id=staff.id)
    
    db.session.add(appt)
    db.session.commit()

    return appt

def update_appt_in_db(form, appt):
    """Update appointment in database"""

    appt.title = form.title.data
    appt.start_date = form.start_date.data
    appt.start_time = form.start_time.data
    appt.end_date = form.start_date.data
    appt.end_time = form.end_time.data
    appt.appt_type = form.type_id.data
    appt.note = form.note.data
    
    appt.category = Category.query.get_or_404(form.category_id.data)

    db.session.commit()
    return appt

def delete_appt_in_db(appt):
    """Delete appointment in database"""

    db.session.delete(appt)
    db.session.commit()
    return appt


#############################################
# Teamup
  
def create_appt_with_teamup_api(appt):
    """Send POST request to Teamup API to create event on calendar"""

    start_dt = f'{appt.start_date}T{appt.start_time}-06:00'
    end_dt = f'{appt.start_date}T{appt.end_time}-06:00'
    category = Category.query.get_or_404(appt.category_id)

    data = {
        "subcalendar_id": category.teamup_id,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "all_day": False,
        "rrule": "",
        "title": appt.title,
        "who": "",
        "location": "",
        "notes": appt.note
    }
    
    event = requests.post(f'{TEAMUP_BASE_URL}/{calendar_id}/events', headers=TEAMUP_POST_HEADERS, data=json.dumps(data))
    get_resp_data = event.text

    id_start = int(get_resp_data.find("id")) + 5
    id_end = id_start + 10
    id_num = get_resp_data[id_start:id_end]
   
    appt.teamup_id = id_num
    db.session.commit() 
    return event

def update_appt_with_teamup_api(appt):
    """Get event from Teamup API, take edit version number from response

    and send it with a PUT request to update appointments on calendar
    """
    category = Category.query.get_or_404(appt.category_id)
    event = requests.get(f'{TEAMUP_BASE_URL}/{calendar_id}/events/{appt.teamup_id}', headers=TEAMUP_GET_HEADERS)
    get_resp_data = event.text

    version_start = int(get_resp_data.find("version")) + 10
    version_end = version_start + 12
    version_num = get_resp_data[version_start:version_end]

    id = str(appt.teamup_id)
    start_dt = f'{appt.start_date}T{appt.start_time}-06:00'
    end_dt = f'{appt.start_date}T{appt.end_time}-06:00'

    data = {
            "id": id,
            "subcalendar_id": category.teamup_id,
            "start_dt": start_dt,
            "end_dt": end_dt,
            "all_day": False,
            "rrule": "",
            "title": appt.title,
            "who": "",
            "location": "",
            "notes": appt.note,
            "version": version_num,
            "redit": None,
            "ristart_dt": None
            }    

    response = requests.put(f'{TEAMUP_BASE_URL}/{calendar_id}/events/{id}', headers=TEAMUP_POST_HEADERS, data=json.dumps(data))
    return response

def delete_appt_on_teamup(appt):

    event = requests.get(f'{TEAMUP_BASE_URL}/{calendar_id}/events/{appt.teamup_id}', headers=TEAMUP_GET_HEADERS)
    get_resp_data = event.text

    version_start = int(get_resp_data.find("version")) + 10
    version_end = version_start + 12
    version_num = get_resp_data[version_start:version_end]

    id = str(appt.teamup_id)

    response = requests.delete(f'{TEAMUP_BASE_URL}/{calendar_id}/events/{id}?version={version_num}&redit=all', headers=TEAMUP_GET_HEADERS)

    return response

#############################################
# Hubspot 

# TODO: V2 to includes API requests to Hubspot API.
def format_hubspot_request(client):
    return {
        "filterGroups":[
            {
                "filters": [
                    {
                        "propertyName": "firstname",
                        "operator": "EQ",
                        # If client arg contains first_name value, assign it here
                        "value": client.first_name
                    },
                    {
                        "propertyName": "lastname",
                        "operator": "NEQ",
                        # If client arg contains first_name value, assign it here
                        "value": client.last_name
                    },
                    {
                        "propertyName": "category",
                        "operator": "EQ",
                        # If client arg contains first_name value, assign it here
                        "value": client.category
                    }
                
                ] 
            },
        ]
    }


