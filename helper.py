from flask import session
from models import db, Staff, Appointment
from secret_keys import TEAMUP_API_KEY
import requests 
from datetime import datetime
from pyteamup import Calendar
import json


api_key = TEAMUP_API_KEY
TEAMUP_BASE_URL = 'https://api.teamup.com'
calendar_id= 'ksov3s6kgmpk6chjah'
SUBCALENDAR_KEYS = {
    'second_appt': 0,
    'annual_review': 1,
    'cancel': 2,
    'Birthdays': 3,
    'Jesses call': 4,
    'out of office': 5,
    'requested_appt_or_policy_delivery': 6,
    'workshop': 7,
}

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
    end_date = form.end_date.data
    end_time = form.end_time.data
    appt_type = form.appt_type.data
    note = form.note.data
    category = form.category.data
    
    staff = Staff.get_users_staff_id(session['user'])

    appt = Appointment(category_id=category, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, title=title, type_id=appt_type, note=note, staff_id=staff.id)
    
    db.session.add(appt)
    db.session.commit()

    return appt


def update_appt_in_db(form, appt):
    """Update appointment in database"""

    appt.title = form.title.data
    appt.start_date = form.start_date.data
    appt.start_time = form.start_time.data
    appt.end_date = form.end_date.data
    appt.end_time = form.end_time.data
    appt.appt_type = form.appt_type.data
    appt.note = form.note.data
    appt.category_id = form.category.data

    db.session.commit()
    return appt


#############################################
# Teamup
  
def create_appt_with_teamup_api(appt):
    """Use library to send request to Teamup API create event on the calendar"""

    calendar = Calendar(calendar_id, api_key)
    subcalendars = calendar.subcalendars
    subcal = subcalendars[appt.category.teamup_id]

    s = datetime.combine(appt.start_date, appt.start_time)
    e = datetime.combine(appt.start_date, appt.end_time)

    new_event_dict = {'title': appt.title,
                    'start_dt': datetime(s.year, s.month, s.day, s.hour, s.minute, 0),
                    'end_dt': datetime(e.year, e.month, e.day, e.hour, e.minute, 0),
                    'subcalendar_ids': subcal['id'],
                    'notes': appt.note}
    new_event = calendar.new_event(**new_event_dict, returnas='event')

    appt.teamup_id = new_event.event_id

    db.session.commit()
    return new_event_dict


def update_appt_with_teamup_api(appt):
    """Get event from Teamup API, take edit version number from response
    and send it with a Put request to update appointments on calendar
    """
    # TODO: Swap hardcoded values for variables 
    event = requests.get(f'https://api.teamup.com/ksov3s6kgmpk6chjah/events/1031392158', headers=TEAMUP_GET_HEADERS)
    get_resp_data = event.json()

    teamup_edit_version_num = get_resp_data["event"]['version']
    
    # TODO: If needed by Teamup, convert these into Dates with ISO-8601 format instead of strings
    start_dt = f'{appt.start_date}T{appt.start_time}-05:00'
    end_dt = f'{appt.start_date}T{appt.end_time}-05:00'

    data = {
            "id": {appt.teamup_id},
            "subcalendar_id": 9387377,
            "start_dt": start_dt,
            "end_dt": end_dt,
            "all_day": False,
            "rrule": "",
            "title": {appt.title},
            "who": "",
            "location": "",
            "notes": {appt.note},
            "version": {teamup_edit_version_num},
            "redit": None,
            "ristart_dt": None
            }
    response = requests.put('https://api.teamup.com/ksov3s6kgmpk6chjah/events/1031392158', headers=TEAMUP_POST_HEADERS, data=data)
    
    print(response.content)
    return response

#############################################
# Hubspot 

# TODO: Finish routes connected to this function
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


