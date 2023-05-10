from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required,  current_user
from . import db
from .models import User,University
import json
from flask_cors import cross_origin

views = Blueprint('views',__name__)


def get_dropdown_values():

    universities = University.query.all()
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

@views.route('/')
def index():

    class_entry_relations = get_dropdown_values()
                        

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    return render_template('index.html',
                       all_classes=default_classes,
                       all_entries=default_values,user=current_user)

@views.route('/_update_dropdown')
@cross_origin()
def update_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)
    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]
    # create the valuesn in the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    print('html_string_selected:', html_string_selected)

    return jsonify(html_string_selected=html_string_selected)


@views.route('/_process_data',methods=['GET','POST'])
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(random_text="You selected the city: {} and the school: {}.".format(selected_class, selected_entry))