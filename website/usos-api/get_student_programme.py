import website.usosapi as usosapi 
import json 
from models import *
import rauth
import requests 
def get_student_programme(university_name):
    base_url = University.query.filter_by(university_name=university_name).first().api_url
    auth_object=usosapi.USOSAPIConnection(base_url,"4ACHmqpSV88bw7fZJANQ","XNeZCccybLfteDAxBYcFe89q4pvsuXgvL5Ah8sH4")
    auth_object._generate_request_token() 
    print(auth_object.get_authorization_url()) 
    pin = input("Podaj PIN: ")
    auth_object.authorize_with_pin(pin) 
    curr = auth_object.get('services/progs/student',active_only='false',old_programs='false')
    json_string = json.dumps(curr)
    return json_string