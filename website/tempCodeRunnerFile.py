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
            new_rating = Rating(username=current_user.username, course_id=course_id,quality_value=quality_value,difficulty_value=difficulty_value,rating_description = review)  #providing the schema for the note 
            db.session.add(new_rating) #adding the rating to the database 
            db.session.commit() 
            api_url = University.query.filter_by(university_name=university_name).first().api_url
            if api_url:
                return redirect(url_for('views.verify_review',university_name=university_name,course_id=course_id)) 
            else:
                return redirect(url_for('views.course',university_name=university_name,course_id=course_id))