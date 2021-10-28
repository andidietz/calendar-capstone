from app import app
from models import db, Category, Type


db.drop_all()

db.create_all()

c1 = Category(
    teamup_id=0,
    category='second appt'
)

c2 = Category(
    teamup_id=1,
    category='annual review'
)

c3 = Category(
    teamup_id=6,
    category='requested appt or policy delivery'
)

c4 = Category(
    teamup_id=7,
    category='workshop'
)

c5 = Category(
    teamup_id=2,
    category='cancelled'
)

t1 = Type(
    appt_type='in person',
)

t2 = Type(
    appt_type='phone',
)

t3 = Type(
    appt_type='zoom',
)


db.session.add_all([c1, c2, c3, c4, c5, t1, t2, t3])
db.session.commit()