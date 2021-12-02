# calendar-capstone
API: https://apidocs.teamup.com/#teamup-api-overview
# The Scheduler #

The Scheduler is an office oriented appointment setting tool. This app helps to break down an information silo within the business to allow different information systems that previously had little to no integration options to be able to freely pass information between themselves. The Scheduler does this by being the main point of information collection so that the data can be stored and sent to various sites through their APIs. Staff can visually see their shared Teamup calendar as well as the appointment setting form on the same page, preventing the need to navigate to multiple windows and sites to create an appointment record. Currently the Scheduler connects to Teamup and will later include an integration with the Hubspot CRM (client relationship management) for appointment record keeping. 


## Features ##
#### Schedule and Reschedule ####
* This feature allows users to create appointments as well as search through previously created appointment in order to update their details.
#### Register/login ####
* This feature ensures that only the people approved to edit the calendar have access to it.
#### Database ####
* The database feature allows for users to search scheduled and reschedule appointment details.
#### Teamup API Integration ####
* The API allows data to be sent to Teamup, a visual, shared calendar used by our office.


## UserFlow ##
![Connecting Calendars Capstone](https://user-images.githubusercontent.com/72045635/144469010-8805adf0-1e24-4229-970e-46f3b151ca52.png)


## Database Schema ##
![Calendar Capstone - DB Schema - Final](https://user-images.githubusercontent.com/72045635/144468863-59b2de90-d521-4e59-886b-c4d69072158c.png)


## API ##
To learn more about the Teamup API, see their docs here. https://apidocs.teamup.com/#teamup-api-overview


## Technology Stack ##
* Flask
* Sqlalchemy 
* Postgresql
* Jinja
* Python 
* Javascript


## Tests ##
To run tests for the Scheduler, enter the command in command line.
* $python3 -m tests.py

