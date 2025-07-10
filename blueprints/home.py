from flask import Blueprint, redirect, url_for, request, render_template, session
from src.User import User

bp = Blueprint("home",__name__,url_prefix="/")

@bp.route("/")
def home():
    return render_template('home.html',session=session) #render template automatically looks for dir named templates and loads respective files from it

@bp.route("/services")
def services():
    return render_template('_services.html',session=session) 

@bp.route("/about")
def about():
    return render_template('_about.html',session=session) 

@bp.route("/contact")
def contact():
    return render_template('_contact.html',session=session) 

@bp.route('/signup')
def signup():
   return render_template('_signup.html') 

@bp.route('/stories')
def stories():
   return render_template('stories.html') 

@bp.route('/blogs')
def blogs():
   return render_template('blogs.html') 