from . import db
from .models import University,Course

def get_dropdown_values():

    universities = University.query.all()
    courses = Course.query.all() 
    for c in courses:
        print(c.university_id)
    # Create an empty dictionary
    myDict = {}
    l=0
    for p in universities:
    
        key = p.location
        location = p.location
        l = l+1
        # Select all car models that belong to a car brand
        q = University.query.filter_by(location=key).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.university_name )
        myDict[key] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations