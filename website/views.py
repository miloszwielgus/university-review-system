from flask import Blueprint, render_template,request,flash,jsonify,url_for,redirect
from flask_login import login_required,  current_user
#from . import db
from .models import *
import json
from flask_cors import cross_origin 
from .functions import *
from sqlalchemy import select

views = Blueprint('views',__name__)


@views.route('/')
def index():

    class_entry_relations = get_university_values()
    all_courses = get_course_values()                  
    courses = Course.query.all() 
    default_courses=[] 
    for course in courses:
        default_courses.append(course.course_name)
    universities = University
    default_classes = sorted(class_entry_relations.keys())
    default_universities = class_entry_relations[default_classes[0]]

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
                course_ids = Course.query.filter(Course.course_name.in_(selected_course)).all()
        elif (selected_university):
               course_ids = Course.query.filter(Course.course_name.in_(selected_course),Course.university_id.in_(university_ids)).all()
        elif (selected_city):
                 unis = University.query.filter(University.location.in_(selected_city)).all()
                 university_ids.clear()
                 for uni in unis: 
                    university_ids.append(uni.university_id)
                 course_ids = Course.query.filter(Course.course_name.in_(selected_course),Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += """<a href="/university/course/{}" 
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">
            Tytuł: {}</p><small>Typ: {}</small></a>""".format(course.course_id,course.course_name,
            University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected)
    
    if(selected_university): 
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += """<a href="/university/course/{}" class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}
            </small></div><p class="mb-1">Tytuł: {}</p><small>Typ: {}</small></a>
            """.format(course.course_id,
                       course.course_name,University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected) 
    
    if(selected_city):
        unis = University.query.filter(University.location.in_(selected_city)).all()
        university_ids.clear()
        for uni in unis: 
            university_ids.append(uni.university_id)
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += """<a href="/university/course/{}" 
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">
            Tytuł: {}</p><small>Typ: {}</small></a>""".format(course.course_id,course.course_name,
            University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected) 

    if  (html_string_selected==''):
        flash('Brak kursów!',category = 'error')
    
    return jsonify(html_string_selected=html_string_selected)

@views.route('/university/<string:university_name>/course/<int:course_id>')
def course(university_name,course_id):
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
                           course=course,course_id=course_id,ratings=ratings,avg_rating=avg_rating,number_of_ratings=number_of_ratings,university_name=university_name,users=users)

@views.route('/university/<string:university_name>')
def university(university_name):
    courses = Course.query.filter_by(university_id=University.query.filter_by(university_name=university_name).first().university_id)
    website = University.query.filter_by(university_name=university_name).first().website
    if university:
        return render_template('university.html',
                            user=current_user,
                            university_name = university_name,website = website,
                            courses=courses)
    else:
         flash('University not found', 'error')
        


@views.route('/style.css')
def style():
    return views.send_static_file('style.css')



@views.route('/university_list')
def uni_list():
    universities = University.query.all()
    cities = [university.location for university in universities]
    user=current_user
    return render_template('uni-list.html', universities=universities, cities=cities, user=user)

@views.route('/_update_university_list', methods=['GET'])
def update_university_list():
    selected_city = json.loads(request.args.get('selected_city'))
    universities = University.query.filter(University.location.in_(selected_city)).all()
    
    html_string_selected = ''
    for university in universities:
        university_link = url_for('views.university', university_name=university.university_name)
        html_string_selected += """
        <div class="list-group-item list-group-item-action flex-column align-items-start active">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1"><a href="{}">{}</a></h5>
          </div>
          <p class="mb-1" >Miasto: {}</p>
          <p class="mb-1">Strona internetowa: <a style="color:black;" href="{}">{}</a></p>
        </div>
        """.format(university_link, university.university_name, university.location, university.website, university.website)

    return jsonify(html_string_selected=html_string_selected)


@views.route('/compare')
def compare():
    # Fetch universities from the database and pass them to the template
    universities = University.query.all()
    return render_template('compare_courses.html', universities=universities, user=current_user)

@views.route('/get_courses')
def get_courses():
    university_id = request.args.get('universityId')
    courses = Course.query.filter_by(university_id=university_id).all()
    courses_data = []
    for course in courses:
        course_data = {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'syllabus': course.syllabus,
            'degree': course.degree,
            'cycle': course.cycle,
            'department': course.department
        }
        courses_data.append(course_data)
    return jsonify(courses_data)

@views.route('/compare_courses')
def compare_courses():
    university1CourseId = request.args.get('university1CourseId')
    university2CourseId = request.args.get('university2CourseId')

    # Retrieve the course information from the database
    course1 = Course.query.get(university1CourseId)
    course2 = Course.query.get(university2CourseId)

    # Retrieve the university information from the database
    university1 = University.query.get(course1.university_id)
    university2 = University.query.get(course2.university_id)

    # Calculate average ratings
    avg_rating1 = calculate_average_rating(course1)
    avg_rating2 = calculate_average_rating(course2)

    # Prepare the data to be returned as JSON
    data = {
        'course1_name': course1.course_name,
        'course2_name': course2.course_name,
        'university1_info': {
            'university_name': university1.university_name if university1 else None,
            'city': university1.location if university1 else None,
            'cycle': course1.cycle,
            'average_rating': avg_rating1
        },
        'university2_info': {
            'university_name': university2.university_name if university2 else None,
            'city': university2.location if university2 else None,
            'cycle': course2.cycle,
            'average_rating': avg_rating2
        }
    }

    return jsonify(data)


def calculate_average_rating(course):
    ratings = Rating.query.filter_by(course_id=course.course_id).all()
    if ratings:
        total_ratings = len(ratings)
        quality_sum = sum(rating.quality_value for rating in ratings)
        average_rating = quality_sum / total_ratings
        return average_rating
    else:
        return 'Brak opinii'

@views.route('/university/<string:university_name>/course/<int:course_id>/add-opinion',methods=['POST','GET'])
def add_opinion(university_name,course_id):
    if request.method == 'POST':
        if(not current_user.is_authenticated):
            return render_template('login.html',user=current_user) 
        difficulty_rating = request.args.get("difficulty")
        quality_rating = request.args.get("quality")
        review = request.args.get("review") 
        new_rating = Rating(username=current_user.username, course_id=course_id,quality_value=quality_rating,difficulty_value=difficulty_rating,rating_description = review)  #providing the schema for the note 
        db.session.add(new_rating) #adding the rating to the database 
        db.session.commit()
        return redirect(url_for('views.course',university_name=university_name,course_id=course_id))

    return render_template('addopinion.html',user=current_user)