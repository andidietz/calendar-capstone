from app import app
from models import db, Category, Type

db.drop_all()
db.create_all()

c1 = Category(
    teamup_id=10285234,
    category='annual review'
)

c2 = Category(
    teamup_id=10285238,
    category='requested appt or policy delivery'
)

c3 = Category(
    teamup_id=10285233,
    category='second appt'
)

c4 = Category(
    teamup_id=10285239,
    category='workshop'
)

c5 = Category(
    teamup_id=10285235,
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