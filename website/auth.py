from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__) 


@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category = 'success')
                login_user(user,remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password!',category = 'error')
        else:
            flash('Wrong email!',category = 'error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get("username")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        user2=User.query.filter_by(username=username).first()
        if user:
            flash('Email taken',category='error')
        elif user2:
            flash('Username taken',category='error')
        elif len(email) < 4:
            flash('Email must be longer than 4',category='error')
        elif len(username) < 2:
             flash('firstName must be longer than 1',category='error')
        elif len(password1) < 7:
             flash('Password must be longer than 6',category='error')
        elif password1 != password2:
             flash('Passwords are not matching',category='error')
        else:
            #add user to database 
            new_user = User(email=email,password=generate_password_hash(password1,method='sha256'),username=username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.index'))
            
    return render_template("sign_up.html",user=current_user)


@auth.route('/about')
def about():
    return render_template("about.html", user=current_user)


@auth.route('/home')
def home():
    return redirect(url_for('views.index'))


@auth.route('/compare-courses')
def compare_courses():
    return render_template("compare-courses.html", user=current_user)


@auth.route('/add-opinion')
def add_opinion():
    return render_template("addopinion.html", user=current_user)


