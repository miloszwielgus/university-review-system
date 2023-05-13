from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150)) 
    username = db.Column(db.String(150))
    rating = relationship("Rating",backref="user")
    

class University(db.Model):
    __tablename__ = 'university'
    university_id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(100), nullable=False)
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
    syllabus = db.Column(db.String(100), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.university_id'), nullable=False)
    rating = relationship("Rating",backref="Course")

    def __repr__(self):
    
        return '\n course_id: {0} course_name: {1} syllabus: {2} university_id: {3}'.format(self.course_id,self.course_name,
                                                                                            self.syllabus,self.university_id)
                                                                    


    def __str__(self):

        return '\n course_id: {0} course_name: {1} syllabus: {2} university_id: {3}'.format(self.course_id,self.course_name,
                                                                                            self.syllabus,self.university_id)


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    rating_description = db.Column(db.String(500))

    def __repr__(self):
    
        return '\n rating_id: {0} user_id: {1} course_id: {2} rating_value: {3} rating_description: {4}'.format(self.rating_id,self.user_id,self.course_id,
                                                                                            self.rating_value,self.rating_description)
                                                                    


    def __str__(self):

       return '\n rating_id: {0} user_id: {1} course_id: {2} rating_value: {3} rating_description: {4}'.format(self.rating_id,self.user_id,self.course_id,
                                                                                            self.rating_value,self.rating_description)

class ChildCourse(ModelView):
    column_list = ['course_id', 'course_name', 'syllabus','university_id']
    form_columns = ['course_name', 'syllabus','university_id']

class ChildRating(ModelView):
    column_list = ['rating_id','user_id','course_id', 'rating_value','rating_description']
    form_columns = ['user_id','course_id', 'rating_value','rating_description']

class ChildUser(ModelView):
    column_list = ['id', 'email', 'password','username']
    form_columns =  ['email', 'password','username']      

class ChildUniversity(ModelView):
    column_list = ['university_id', 'university_name', 'location','website'] 
    form_columns = [ 'university_name', 'location','website']
