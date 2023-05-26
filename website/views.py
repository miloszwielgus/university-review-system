from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required,  current_user
#from . import db
from .models import *
import json
from flask_cors import cross_origin 
from .functions import *
from sqlalchemy import select

views = Blueprint('views',__name__)



@views.route('/uni-list')
def uni_list():
    class_entry_relations = get_university_values()
    all_courses = get_course_values()
    courses = Course.query.all()
    universities = University
    default_classes = sorted(class_entry_relations.keys())
    default_universities = class_entry_relations[default_classes[0]]
    default_courses = all_courses[class_entry_relations[default_classes[0]][0]]

    return render_template('uni-list.html',
                       all_cities=default_classes,
                       all_universities=default_universities,all_courses=default_courses,default_courses=default_courses,user=current_user,courses=courses,universities=universities)

@views.route('/')
def index():

    class_entry_relations = get_university_values()
    all_courses = get_course_values()
    courses = Course.query.all()
    universities = University
    default_classes = sorted(class_entry_relations.keys())
    default_universities = class_entry_relations[default_classes[0]]
    default_courses = all_courses[class_entry_relations[default_classes[0]][0]]

    return render_template('index.html',
                       all_cities=default_classes,
                       all_universities=default_universities,all_courses=default_courses,default_courses=default_courses,user=current_user,courses=courses,universities=universities)

@views.route('/_update_university_dropdown')
@cross_origin()
def update_university_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_city = json.loads(request.args.get('selected_city'))
    # get values for the second dropdown
    html_string_selected = ''
    for city in selected_city:
       updated_values = get_university_values()[city]
       for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
    # create the valuesn in the dropdown as a html string
    

    
    #print('html_string_selected:', html_string_selected)

    return jsonify(html_string_selected=html_string_selected)

@views.route('/_update_course_dropdown')
@cross_origin()
def update_course_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_university = json.loads(request.args.get('selected_university'))
    
    html_string_selected = ''
    # get values for the second dropdown
    for university in selected_university:
        updated_values = get_course_values()[university]
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
    # create the valuesn in the dropdown as a html string

    #print('html_string_selected:', html_string_selected)

    return jsonify(html_string_selected=html_string_selected)


@views.route('/_update_course_list',methods=['GET','POST'])
def update_course_list():
    selected_city = json.loads(request.args.get('selected_city'))
    selected_university = json.loads(request.args.get('selected_university'))
    selected_course = json.loads(request.args.get('selected_course')) 
    universities = University.query.filter(University.university_name.in_(selected_university)).all() 
    
    university_ids = []
    for uni in universities: 
         university_ids.append(uni.university_id)
    html_string_selected = ''

    if(selected_course):
        course_ids = []  
        if (not selected_city and not selected_university):
               # course_ids =  select(Course).where(Course.course_name.in_(selected_course))  
                course_ids = Course.query.filter(Course.course_name.in_(selected_course)).all()
        elif (selected_university):
               # course_ids =  select(Course).where(Course.course_name.in_(selected_course)).where(Course.university_id.in_(university_ids.university_id)) 
               course_ids = Course.query.filter(Course.course_name.in_(selected_course),Course.university_id.in_(university_ids)).all()
        elif (selected_city):
                #course_ids = select(Course).where(Course.course_name.in_(selected_course)).where(
                 #                                 Course.university_id.in_(select(University.university_id).where(University.location.in_(selected_city))))
                 unis = University.query.filter(University.location.in_(selected_city)).all()
                 university_ids.clear()
                 for uni in unis: 
                    university_ids.append(uni.university_id)
                 course_ids = Course.query.filter(Course.course_name.in_(selected_course),Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += '<a href="/university/course/{}" class="list-group-item list-group-item-action flex-column align-items-start active"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">Tytuł: {}</p><small>Typ: {}</small></a>'.format(course.course_id,course.course_name,University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected)
    
    if(selected_university): 
        #course_ids = select(Course).where(Course.university_id.in_(select(University.university_id).where(University.university_name.in_(selected_university))))
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += '<a href="/university/course/{}" class="list-group-item list-group-item-action flex-column align-items-start active"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">Tytuł: {}</p><small>Typ: {}</small></a>'.format(course.course_id,course.course_name,University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected) 
    
    if(selected_city):
        unis = University.query.filter(University.location.in_(selected_city)).all()
        university_ids.clear()
        for uni in unis: 
            university_ids.append(uni.university_id)
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += '<a href="/university/course/{}" class="list-group-item list-group-item-action flex-column align-items-start active"><div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">Tytuł: {}</p><small>Typ: {}</small></a>'.format(course.course_id,course.course_name,University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected) 

    if  (html_string_selected==''):
        flash('Brak kursów!',category = 'error')
    
    return jsonify(html_string_selected=html_string_selected)

@views.route('/university/course/<int:course_id>')
def course(course_id):
    ratings = Rating.query.filter_by(course_id=course_id).all()
    course = Course.query.filter_by(course_id = course_id).first()
    university_name = University.query.filter_by(university_id =course.university_id).first().university_name 
    users = User.query.all()
    avg_rating = 0
    number_of_ratings = 0               #to do: implement a better mechanism for avg_rating (it should be stored somewhere and updated)
    for rating in ratings:
        avg_rating += (rating.quality_value + rating.difficulty_value)
        number_of_ratings += 1 
    if number_of_ratings != 0:
        avg_rating /= (number_of_ratings*2) 

    return render_template('course.html',
                           user=current_user,
                           course=course,ratings=ratings,avg_rating=avg_rating,number_of_ratings=number_of_ratings,university_name=university_name,users=users)

@views.route('/university/<string:university_name>')
def university(university_name):
    courses = Course.query.filter_by(university_id=University.query.filter_by(university_name=university_name).first().university_id)
    website = University.query.filter_by(university_name=university_name).first().website
    return render_template('university.html',
                           user=current_user,
                           university_name = university_name,website = website,
                           courses=courses)

@views.route('/style.css')
def style():
    return views.send_static_file('style.css')


