from app import db
from sqlalchemy import Numeric

from sqlalchemy import func, event, DDL

from app import db
from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    learns = relationship('Learn', backref='user', lazy='dynamic')
    fits = relationship('Fit', backref='user', lazy='dynamic')
    bodies = relationship('Body', backref='user', lazy='dynamic')
    eats = relationship('Eat', backref='user', lazy='dynamic')
    variouss = relationship('Various', backref='user', lazy='dynamic')

class Learn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)

class Fit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise = db.Column(db.String(150), nullable=False)
    exercise_count = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)

class Body(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weight = db.Column(db.Float(precision=4), nullable=True)
    weist = db.Column(db.Float(precision=4), nullable=True)
    bicep = db.Column(db.Float(precision=4), nullable=True)
    glucose = db.Column(db.Float(precision=4), nullable=True)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)

class Eat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal = db.Column(db.String(500), nullable=False)
    comment = db.Column(db.String(150), nullable=True)
    time_delta = db.Column(db.Interval)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    weight = db.Column(db.Float(precision=4), nullable=True)

class Various(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    week_goal = db.Column(db.Integer, server_default="600")
