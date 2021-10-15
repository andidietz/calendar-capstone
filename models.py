from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    title = db.Column(db.String(60), nullable=False)
    note = db.Column(db.Text)
    staff_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    teamup_id = db.Column(db.Integer)

    # categories = db.relationship("Category", secondary='Apppointment_Category')

class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    @classmethod
    def register(cls, full_name, email, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        return cls(full_name=full_name, email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, email, pwd):
        staff_member = cls.query.filter_by(email=email).first()
        print('autho')
        if staff_member and bcrypt.check_password_hash(staff_member.password, pwd):
            return staff_member
        else:
            return False
            
    @classmethod
    def get_users_staff_id(cls, username):
        return Staff.query.filter_by(full_name=username).one()


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    hubspot_id = db.Column(db.Integer, nullable=False)


class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    appt_type = db.Column(db.Text, nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.Text, nullable=False)
    teamup_id = db.Column(db.Integer)


class Apppointment_Category(db.Model):
    __tablename__='appointments_categories'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    appt_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
