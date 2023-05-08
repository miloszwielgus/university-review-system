from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required,  current_user
from . import db
from .models import User
import json

views = Blueprint('views',__name__)

@views.route('/home',methods=['GET','POST'])
def home():
    return render_template("home.html",user=current_user)