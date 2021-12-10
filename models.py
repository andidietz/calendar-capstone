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
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    
    @classmethod
    def register(cls, full_name, email, pwd, admin):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        return cls(full_name=full_name, email=email, password=hashed_utf8, admin=admin)

    @classmethod
    def authenticate(cls, email, pwd):
        staff_member = cls.query.filter_by(email=email).first()
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
    category = db.Column(db.Text)
    teamup_id = db.Column(db.Integer)

    appointments = db.relationship('Appointment', backref='category', cascade="all, delete-orphan")
