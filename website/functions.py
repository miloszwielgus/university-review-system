from . import db
from .models import University,Course,Rating
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_university_values():

    universities = University.query.all() 
    myDict = {} 
    for p in universities:
        key = p.location
        q = University.query.filter_by(location=key).all()
        lst_c = []
        for c in q:
            lst_c.append( c.university_name )
        myDict[key] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 

def get_course_values():

    universities = University.query.all()
    
    myDict = {} 
    for p in universities:
    
        key = p.university_id
        
        q = Course.query.filter_by(university_id=key).all()
    
        
        lst_c = []
        for c in q:
            lst_c.append( c.course_name)
        myDict[p.university_name] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 



def send_email(sender_email, sender_password, recipient_email, subject, message):
    smtp_server = "smtp.poczta.onet.pl" #tu podajemy adres serwera smtp poczty wysylajacego, adresy innych domen tutaj: https://www.blulink.pl/serwery-poczty-smtp,-pop3,-imap,125.html
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
    ratings = course.rating  
    total_ratings = len(ratings)
    if total_ratings == 0:
        return 0

    sum_quality_values = sum(rating.quality_value for rating in ratings)
    average_quality_value = sum_quality_values / total_ratings
    return average_quality_value


def calculate_average_difficulty_value(course):
    ratings = course.rating  
    total_ratings = len(ratings)

    if total_ratings == 0:
        return 0

    sum_difficulty_values = sum(rating.difficulty_value for rating in ratings)
    average_difficulty_value = sum_difficulty_values / total_ratings

    return average_difficulty_value

def calculate_average_rating(course):
    ratings = Rating.query.filter_by(course_id=course.course_id).all()
    if ratings:
        total_ratings = len(ratings)
        quality_sum = sum(rating.quality_value for rating in ratings)
        average_rating = quality_sum / total_ratings
        return round(average_rating,2)
    else:
        return 'Brak opinii'