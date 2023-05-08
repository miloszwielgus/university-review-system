from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150)) 
    username = db.Column(db.String(150))

class University(db.Model):
    __tablename__ = 'university'
    university_id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(100), nullable=False)

    def __unicode__(self):
        return self.university_id or ''

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    syllabus = db.Column(db.String(100), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.university_id'), nullable=False)
    university = db.relationship('University', backref=db.backref('university', lazy=True))

class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    rating_description = db.Column(db.String(500))
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    course = db.relationship('Course', backref=db.backref('course', lazy=True))



