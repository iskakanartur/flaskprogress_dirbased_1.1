from app import db

from sqlalchemy import func, event, DDL

## For the track progess project remove this (later )
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)





class Learn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)


class fit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(150), nullable=False)
    count = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)

class eat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(500), nullable=False)
    drink = db.Column(db.String(500), nullable=False)
    drink_count = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # fasted = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)



class various(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    week_goal  = db.Column(db.Integer,  server_default="600")




## This is to set a default value 600 learning hours to the table various
## CAREFUL !!! The table already exists: If the various table already exists in your database, 
## running db.create_all() won’t modify the existing table
event.listen(
    various.__table__,
    'after_create',
    DDL("INSERT INTO various (id) VALUES (1)")
)