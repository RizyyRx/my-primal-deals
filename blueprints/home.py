from flask import Blueprint, redirect, url_for, request, render_template, session
from src.User import User

bp = Blueprint("home",__name__,url_prefix="/")

@bp.route("/")
def home():
    return render_template('home.html')

@bp.route('/dashboard')
def dashboard():
   return render_template('dashboard.html',session=session) #render template automatically looks for dir named templates and loads respective files from it

@bp.route('/signup')
def signup():
   return render_template('_signup.html') #render template automatically looks for dir named templates and loads respective files from it