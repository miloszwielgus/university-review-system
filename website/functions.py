from . import db
from .models import University,Course

def get_university_values():

    universities = University.query.all()
    courses = Course.query.all()
    # Create an empty dictionary
    myDict = {} 
    coursesDict = {}
    l=0
    for p in universities:
    
        key = p.location
        # Select all car models that belong to a car brand
        q = University.query.filter_by(location=key).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.university_name )
        myDict[key] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 

def get_course_values():

    universities = University.query.all()
    # Create an empty dictionary
    myDict = {} 
    for p in universities:
    
        key = p.university_id
        # Select all car models that belong to a car brand
        q = Course.query.filter_by(university_id=key).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.course_name)
        myDict[p.university_name] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 
