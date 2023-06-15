"""
This file is a part of the University Review System project.
https://github.com/miloszwielgus/university-review-system
Please acknowledge the original authors if you use or modify this code.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask import Flask, request
from flask_mail import Mail, Message
from flask_login import login_user, login_required, logout_user, current_user
from .functions import *


auth = Blueprint('auth',__name__) 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login page functionality.

    Function retrieves the email and password from the user.
    It checks if the user already exists and verifies the password.
    If the login is successful, the user is logged in, and they are redirected to the home page.
    Otherwise, appropriate error messages are flashed.
    If the request method is GET, it renders the login page.
    """
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
    """
    Handles the logout functionality.

    Logs out the currently logged-in user and redirects to the login page.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    """
    Handles the user registration functionality.

    Retrieves the email, username, and passwords from the user.
    It checks if the email and username are already taken and validates the input data.
    If everything is valid, a new user is created and added to the database.
    The new user is then logged in, and the user is redirected to the home page.
    """
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
            new_user = User(email=email,password=generate_password_hash(password1,method='sha256'),username=username,is_admin=0)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!',category='success')
            send_email("max11@spoko.pl","",email,"Dziękujemy za rejestrację",f"Dziekujemy za rejestracje na portalu MyśliStudenta, twój nick to: {username}")
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


@auth.route("/send_question", methods=["POST"])
def send_question():
    # Get form data
    sender_email = "max11@spoko.pl"  # Tu podaj swój adres email
    sender_password = ""  # Tu podaj hasło do swojego konta email
    recipient_email = "izka.golec@gmail.com"  # Adres e-mail odbiorcy (zmieniony na izka.golec@gmail.com)
    subject = "Pytanie od: " + request.form["email"]
    message = request.form["question"]

    # Send email
    send_email(sender_email, sender_password, recipient_email, subject, message)

    return "Pytanie zostało wysłane."
