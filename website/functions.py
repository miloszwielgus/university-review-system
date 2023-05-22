from . import db
from .models import University,Course
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_university_values():

    universities = University.query.all()
    # Create an empty dictionary
    myDict = {} 
    for p in universities:
    
        key = p.location
        # Select all car models that belong to a car brand
        q = University.query.filter_by(location=key).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.university_name )
        myDict[key] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 

def get_course_values():

    universities = University.query.all()
    # Create an empty dictionary
    myDict = {} 
    for p in universities:
    
        key = p.university_id
        # Select all car models that belong to a car brand
        q = Course.query.filter_by(university_id=key).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.course_name)
        myDict[p.university_name] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations 



def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the SMTP server
    smtp_server = "smtp.example.com"
    smtp_port = 587

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Add body to email
    msg.attach(MIMEText(message, "plain"))

    try:
        # Log in to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return
    finally:
        # Close the SMTP server connection
        server.quit()