from src.User import User
from src.Session import Session
from flask import Blueprint, redirect, url_for, request, render_template, session

bp = Blueprint("apiv1",__name__,url_prefix="/api/v1")

@bp.route('/register',methods=['POST'])
def register():
   if 'username' in request.form and 'password' in request.form and 'name' in request.form and 'email' in request.form:
      username = request.form['username']
      password = request.form['password']
      name = request.form['name']
      email = request.form['email']

      try:
         uid = User.register(username,password,password,name,email)
         return redirect(url_for('home.dashboard'))
      except Exception as e:
         return{
            "message": str(e),
         }, 400
   else:
      return {
         "message": "Not enough parameters",
      }, 400


@bp.route('/auth',methods=['POST'])
def auth():
   if session.get('authenticated'):
      print(session)
      sess = Session(session['sessid']) # create a session instance with sessid present in flask's session object
      if sess.is_valid():
         return{
            "message":"Already authenticated",
            "authenticated":True
         }, 202 #already authed
      else:
         session['authenticated'] = False # set authenticated to false in flask session object
         sess.collection.active = False # set active to false directly in db since sess inherits the mongogettersetter metaclass and sess.collection will have the session collection
         return{
            "message":"Session expired",
            "authenticated":False
         }, 401
   else: 
      if 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         try:
            sessid = User.login(username,password) # sessid is retrieved here from the Session object created while registering session
            #These are flask's session (session is flask's session object)
            session['authenticated'] = True
            session['username'] = username
            session['sessid'] = sessid # put sessid, created when registering session in flask's session object. It will be used to reconstruct the session instance using id and check if its valid, if authenticated is True
            session['type'] = 'web' # if user authenticated thru web, set this variable

            return redirect(url_for('home.dashboard')) # redirect to dashboard if login is successful
         except Exception as e:
            return{
               "message":str(e),
               "authenticated":False
            }, 401 # not authed
      else:
         return{
            "message":"Not enough parameters",
            "authenticated":False
         }, 400 # bad request
      

@bp.route('/deauth')
def deauth():
   session['authenticated'] = False
   session['type'] = None
   # return{
   #    "message":"successfully deauthed",
   #    "authenticated":False
   # }, 200
   return redirect(url_for('home.dashboard'))