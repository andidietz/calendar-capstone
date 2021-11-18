from unittest import TestCase

from app import app
from models import db, Appointment, Staff

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calendar_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    def setUp(self):
        Staff.query.delete()
        Appointment.query.delete()

        staff = Staff.register(full_name='Test Staff', email='test@test.com', password='password')
        appt = Appointment(teamup_id=1, category_id=1, start_date='2021-11-12', start_time='6:00:00', end_date='2021-11-12', end_time='6:30:00', title='Setup Test Title', type_id=1, note='Test Note', staff_id=self.staff_id)
        
        db.session.add(staff, appt)
        db.session.commit()

        self.client = app.test_client()
        self.staff_id = staff.id
        self.appt = appt
    
    def tearDown(self):
        db.session.rollback()
    
    def test_add_appointment_in_db(self):
        appt = Appointment(category_id=1, start_date='2021-11-12', start_time='6:00:00', end_date='2021-11-12', end_time='6:30:00', title='Test Title - Add Appt Test', type_id=1, note='Test Note', staff_id=self.staff_id)
        db.session.add(appt)
        db.session.commit()

        appt_in_db = Appointment.query.filter_by(title='Test Title - Add Appt Test').one()
        self.assertEquals(appt_in_db, appt)

    def test_schedule_route(self):
            resp = self.client.get('/schedule/add')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Start Date', html)

    def test_reschedule_route(self):
            resp = self.client.get(f'/{self.appt.id}/update')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Start Date', html)

    def test_reschedule_route(self):
            resp = self.client.get('/reschedule/search')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('search title of appoinment', html)

    def test_all_desserts(self):
            resp = self.client.get('/api/reschedule/search?q=Setup')
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                {'id':self.appt.id,
                'teamup_id':1,
                'category':1,
                'start_date':'2021-11-12',
                'start_time':'6:00:00',
                'end_date':'2021-11-12',
                'end_time':'6:30:00',
                'title':'Setup Test Title',
                'note':'Test Note'
                })