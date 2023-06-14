"""
This file is a part of the University Review System project.
https://github.com/miloszwielgus/university-review-system
Please acknowledge the original authors if you use or modify this code.
"""
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship 
from .admin import AdminView



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150)) 
    username = db.Column(db.String(150))
    is_admin = db.Column(db.Integer)

    rating = relationship("Rating",backref="user")
    


class University(db.Model):
    __tablename__ = 'university'
    university_id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(100), nullable=False) 
    api_url = db.Column(db.String(50))
    course = relationship("Course",backref = "University")


    def __repr__(self):
    
        return '\n university_id: {0} university_name: {1} location: {2} website: {3}'.format(self.university_id,
                                                                    self.university_name, self.location, self.website)

    def __str__(self):

        return '\n university_id: {0} university_name: {1} location: {2} website: {3}'.format(self.university_id,
                                                                    self.university_name, self.location, self.website)


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    syllabus = db.Column(db.String(200), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.university_id'), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    cycle = db.Column(db.String(100), nullable=False) 
    department = db.Column(db.String(100)) 
    code = db.Column(db.String(50))
    rating = relationship("Rating",backref="Course")

    def __repr__(self):
    
        return '\n course_id: {0} course_name: {1} syllabus: {2} university_id: {3} degree: {4} cycle: {5}'.format(self.course_id,self.course_name,
                                                                                            self.syllabus,self.university_id,self.degree,self.cycle)
                                                                    



    def __str__(self):

        return '\n course_id: {0} course_name: {1} syllabus: {2} university_id: {3} degree: {4} cycle: {5}'.format(self.course_id,self.course_name,
                                                                                            self.syllabus,self.university_id,self.degree,self.cycle)


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    quality_value = db.Column(db.Integer, nullable=False)
    difficulty_value = db.Column(db.Integer, nullable=False)
    rating_description = db.Column(db.String(500)) 
    is_verified = db.Column(db.Integer)
    def __repr__(self):
    
        return '\n rating_id: {0} username: {1} course_id: {2} rating_value: {3} rating_description: {4}'.format(self.rating_id,self.username,self.course_id,
                                                                                            self.quality_value,self.rating_description)

    def __str__(self):

       return '\n rating_id: {0} username: {1} course_id: {2} rating_value: {3} rating_description: {4}'.format(self.rating_id,self.username,self.course_id,self.quality_value,self.rating_description)
    
  



class ChildCourse(AdminView):
    column_list = ['course_id', 'course_name', 'syllabus','university_id','degree','cycle','department','code']
    form_columns = ['course_name', 'syllabus','university_id','degree','cycle','department','code']

    

class ChildRating(AdminView):
    column_list = ['rating_id','username','course_id', 'quality_value','difficulty_value','rating_description','is_verified']
    form_columns = ['username','course_id', 'quality_value','difficulty_value','rating_description','is_verified']

class ChildUser(AdminView):
    column_list = ['id', 'email', 'password','username','is_admin']
    form_columns =  ['email', 'password','username','is_admin']      

class ChildUniversity(AdminView):
    column_list = ['university_id', 'university_name', 'location','website','api_url'] 
    form_columns = [ 'university_name', 'location','website','api_url']

