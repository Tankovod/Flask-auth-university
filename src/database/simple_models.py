from flask_login import UserMixin

from ..settings import settings

db = settings.db_lite


class UserSite(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=False)
    date_of_birth = db.Column(db.DateTime, unique=False)
    university_id = db.Column(db.Integer)
    year_of_admission = db.Column(db.Integer)


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True)
    short_name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, unique=False)


