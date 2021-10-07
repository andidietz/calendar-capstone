from app import app
from models import db, Category, Type


db.drop_all()
db.create_all()

c1 = Category(
    teamup_id=9387377,
    category='second appt'
)

c2 = Category(
    teamup_id=9382928,
    category='annual review'
)

c3 = Category(
    teamup_id=9381286,
    category='requested appt or policy delivery'
)

c4 = Category(
    teamup_id=9381285,
    category='workshop'
)

c5 = Category(
    teamup_id=9387837,
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


db.session.add_all([c1, c2, c3, c4, t1, t2, t3])
db.session.commit()