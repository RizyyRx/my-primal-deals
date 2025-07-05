import sys
sys.path.append('/home/rizwankendo/myPrimalDeals') # this will help to find the app.py for deployment server 

from flask import Flask, redirect, url_for, request, render_template, session
import os
import math
from src import get_config
from src.User import User
from blueprints import home, api

'''
 * by using static_folder='assets', static_url_path=basename, now all the contents inside assets will be available in the basename iot/ in website.
 * the assets dir is kept static
 * put application, coz wsgi looks for var named application by default that has the flask object
'''
application = app = Flask(__name__, static_folder='static', static_url_path="/static") #app is an object being created of class Flask  
app.secret_key = get_config("secret_key") # flask uses this key to auth session

app.register_blueprint(home.bp)
app.register_blueprint(api.bp)

if __name__ == '__main__': #name == main checks that if this is the main file or not
   app.run(host="0.0.0.0", port=5000,debug=True)