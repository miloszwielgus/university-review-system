from flask import Blueprint, render_template,request,flash,jsonify,url_for,redirect, session
from flask_login import login_required,  current_user
from .models import * 
import redis
import json
from flask_cors import cross_origin 
from .functions import *
from sqlalchemy import select 
from . import usosapi
from .functions import calculate_average_difficulty_value, calculate_average_quality_value, calculate_average_rating
views = Blueprint('views',__name__)

global_auth_object = None

def get_auth_object(base_url):
    global global_auth_object

    if global_auth_object is None:
        
         global_auth_object=usosapi.USOSAPIConnection(base_url,"4ACHmqpSV88bw7fZJANQ","XNeZCccybLfteDAxBYcFe89q4pvsuXgvL5Ah8sH4")
    return global_auth_object

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
    
    selected_city = json.loads(request.args.get('selected_city'))
    html_string_selected = ''
    for city in selected_city:
       updated_values = get_university_values()[city]
       for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)

@views.route('/_update_course_dropdown')
@cross_origin()
def update_course_dropdown():
    
    selected_university = json.loads(request.args.get('selected_university'))
    
    html_string_selected = ''
    
    for university in selected_university:
        updated_values = get_course_values()[university]
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

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
            html_string_selected += """<a href="/university/{}/course/{}"
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">
            Tytuł: {}</p><small>Typ: {}</small></a>""".format(University.query.filter_by(university_id=course.university_id).first().university_name,course.course_id,course.course_name,
            University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected)
    
    if(selected_university): 
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += """<a href="/university/{}/course/{}" class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}
            </small></div><p class="mb-1">Tytuł: {}</p><small>Typ: {}</small></a>
            """.format(University.query.filter_by(university_id=course.university_id).first().university_name,course.course_id,
                       course.course_name,University.query.filter_by(university_id=course.university_id).first().university_name,course.degree,course.cycle)
        return jsonify(html_string_selected=html_string_selected) 
    
    if(selected_city):
        unis = University.query.filter(University.location.in_(selected_city)).all()
        university_ids.clear()
        for uni in unis: 
            university_ids.append(uni.university_id)
        course_ids = Course.query.filter(Course.university_id.in_(university_ids)).all()
        for course in course_ids:
            html_string_selected += """<a href="/university/{}/course/{}" 
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{}</h5><small>{}</small></div><p class="mb-1">
            Tytuł: {}</p><small>Typ: {}</small></a>""".format(University.query.filter_by(university_id=course.university_id).first().university_name,course.course_id,course.course_name,
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
    avg_rating = calculate_average_rating(course)
    ratings = Rating.query.filter_by(course_id=course_id).all()
    number_of_ratings = len(ratings)  
    avg_quality_value = (100*calculate_average_quality_value(course))/5
    avg_difficulty_value = (100*calculate_average_difficulty_value(course))/5
   
    return render_template('course.html',
                           user=current_user,
                           course=course,course_id=course_id,ratings=ratings,avg_rating=avg_rating,number_of_ratings=number_of_ratings,university_name=university_name,users=users, avg_quality_value=avg_quality_value,
                           avg_difficulty_value=avg_difficulty_value)

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
    course1 = Course.query.get(university1CourseId)
    course2 = Course.query.get(university2CourseId)
    university1 = University.query.get(course1.university_id)
    university2 = University.query.get(course2.university_id)
    avg_rating1 = calculate_average_rating(course1)
    avg_rating2 = calculate_average_rating(course2)

    data = {
        'course1_name': course1.course_name,
        'course2_name': course2.course_name,
        'university1_info': {
            'university_name': university1.university_name if university1 else None,
            'city': university1.location if university1 else None,
            'cycle': course1.cycle,
            'average_rating': avg_rating1,
            'nr_of_ratings':len(Rating.query.filter_by(course_id=course1.course_id).all())
        },
        'university2_info': {
            'university_name': university2.university_name if university2 else None,
            'city': university2.location if university2 else None,
            'cycle': course2.cycle,
            'average_rating': avg_rating2,
            'nr_of_ratings': len(Rating.query.filter_by(course_id=course2.course_id).all())
        }
    }

    return jsonify(data)


@views.route('/top_universities')
def top_universities():
    
    universities = University.query.all()
    universities_avg_rating = []
    for university in universities:
        courses = Course.query.filter_by(university_id=university.university_id).all()
        total_rating = 0
        course_count = 0
        for course in courses:
            for rating in course.rating:
                total_rating += rating.quality_value  
                course_count += 1
        avg_rating = total_rating / course_count if course_count > 0 else 0
        universities_avg_rating.append((university, round(avg_rating,2)))

    
    universities_avg_rating.sort(key=lambda x: x[1], reverse=True)
    top_universities = universities_avg_rating[:5]

    return render_template('top_universities.html', universities=top_universities, user=current_user)


@views.route('/university/<string:university_name>/course/<int:course_id>/add-opinion',methods=['POST','GET'])
def add_opinion_page(course_id,university_name):
    if(not current_user.is_authenticated):
                return render_template('login.html',user=current_user) 
    if(Rating.query.filter(Rating.course_id == course_id,Rating.username == current_user.username).first()):
                flash("Dodałeś już opinię na temat tego kursu","error")
                return redirect(url_for('views.course',university_name=university_name,course_id=course_id))
    return render_template('addopinion.html',user=current_user,course_id=course_id,university_name=university_name)

@views.route('/university/<string:university_name>/course/<int:course_id>/add-opinion/verify_review')
def verify_review(course_id,university_name): 
    base_url = University.query.filter_by(university_name=university_name).first().api_url
    auth_object = get_auth_object(base_url)
    auth_object._generate_request_token() 
    auth_url = auth_object.get_authorization_url() 
    return render_template('verify_review.html',course_id=course_id,university_name=university_name,user=current_user,auth_url=auth_url,auth_object=auth_object)
    

@views.route('/_process_pin',methods=['POST'])
def process_pin(): 
        pin = request.form.get('pin_input') 
        course_id = request.form.get('course_id') 
        university_name = request.form.get('university_name')
        auth_object = get_auth_object('base_url')
        auth_object.authorize_with_pin(pin) 
        curr = auth_object.get('services/progs/student',active_only='false',old_programs='false')
        json_string = json.dumps(curr)
        course_code = json.loads(json_string)
        course_code = course_code[0]['programme']['id']
        if course_code == Course.query.filter_by(course_id=course_id).first().code:
             rating = Rating.query.filter(Rating.course_id == course_id, Rating.username == current_user.username).first()
             print(rating.is_verified)
             rating.is_verified = 1
             db.session.commit()
        response = url_for('views.course',course_id=course_id,university_name=university_name)
        return response

@views.route('/_add_opinion',methods=['POST'])
def add_opinion():
        if request.method == 'POST':
            if(not current_user.is_authenticated):
                return render_template('login.html',user=current_user) 
            university_name=request.form.get('university_name')
            course_id=request.form.get('course_id') 
            review=request.form.get('review')
            difficulty_value=request.form.get('difficulty_value')
            quality_value=request.form.get('quality_value')
            new_rating = Rating(username=current_user.username, course_id=course_id,quality_value=quality_value,difficulty_value=difficulty_value,rating_description = review,is_verified = 0)  
            db.session.add(new_rating) 
            db.session.commit() 
            api_url = University.query.filter_by(university_name=university_name).first().api_url 
            course_url = url_for('views.course',university_name=university_name,course_id=course_id)
            if api_url:
             redirection_url = url_for('views.verify_review',course_id=course_id,university_name=university_name)
             return redirection_url
            else:
                 return course_url


