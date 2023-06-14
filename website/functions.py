"""
This file is a part of the University Review System project.
https://github.com/miloszwielgus/university-review-system
Please acknowledge the original authors if you use or modify this code.
"""
from . import db
from .models import University,Course,Rating
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request
from flask_mail import Mail, Message

def get_university_values():
    """
    Retrieves and organizes university values from the database.

    Returns:
    A dictionary containing university locations as keys and a list of associated university names as values.
    """

    universities = University.query.all()
    university_dict = {}

    for university in universities:
        location = university.location
        universities_at_location = University.query.filter_by(location=location).all()
        university_names = []

        for uni in universities_at_location:
            university_names.append(uni.university_name)

        university_dict[location] = university_names

    return university_dict

def get_course_values():
    """
    Retrieves and organizes course values from the database.

    Returns:
    A dictionary containing university names as keys and a list of associated course names as values.
    """
    universities = University.query.all()
    course_dict = {}

    for university in universities:
        university_id = university.university_id
        courses = Course.query.filter_by(university_id=university_id).all()
        course_names = []

        for course in courses:
            course_names.append(course.course_name)

        course_dict[university.university_name] = course_names

    return course_dict



def send_email(sender_email, sender_password, recipient_email, subject, message):
    """
    Sends an email using the provided sender and recipient email addresses,
    along with the subject and message.

    """
    smtp_server = "smtp.poczta.onet.pl" #other domain addresses can be found here: https://www.blulink.pl/serwery-poczty-smtp,-pop3,-imap,125.html
    smtp_port = 587
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return
    finally:
        server.quit()


def calculate_average_quality_value(course):
    """
    Calculates the average quality value for a given course based on its ratings.

    Returns:
    float: The average quality value for the course.
    """
    ratings = course.rating  
    total_ratings = len(ratings)
    if total_ratings == 0:
        return 0

    sum_quality_values = sum(rating.quality_value for rating in ratings)
    average_quality_value = sum_quality_values / total_ratings
    return average_quality_value


def calculate_average_difficulty_value(course):
    """
    Calculates the average difficulty value for a given course based on its ratings.

    Returns:
    float: The average difficulty value for the course.
    """
    
    ratings = course.rating  
    total_ratings = len(ratings)

    if total_ratings == 0:
        return 0

    sum_difficulty_values = sum(rating.difficulty_value for rating in ratings)
    average_difficulty_value = sum_difficulty_values / total_ratings

    return average_difficulty_value

def calculate_average_rating(course):
    """
    Calculates the average rating for a given course based on its ratings.

    Returns:
    float or str: The average rating for the course, rounded to two decimal places,
                 or 'Brak opinii' (No reviews) if there are no ratings.
    """
    ratings = Rating.query.filter_by(course_id=course.course_id).all()
    if ratings:
        total_ratings = len(ratings)
        quality_sum = sum(rating.quality_value for rating in ratings)
        average_rating = quality_sum / total_ratings
        return round(average_rating,2)
    else:
        return 'Brak opinii'

