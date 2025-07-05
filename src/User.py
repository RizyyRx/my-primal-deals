from src.Database import Database
from src import get_config
from src.Session import Session
from time import time
from random import randint
import binascii
import bcrypt
from flask import Blueprint, redirect, url_for, request, render_template, session
from mongogettersetter import MongoGetterSetter
from uuid import uuid4


db = Database.get_connection()
users = db.users # create a collection of users if it doesnt exists

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self, username):
        self._collection = db.users
        self._filter_query = {
            "$or": [
                {"username":username},
                {"id":username}
            ]
        }

class User:
    def __init__(self, id):
        self.collection = UserCollection(id)
        self.id = self.collection.id
        self.username = self.collection.username

    @staticmethod
    def register(username, password, confirm_password, name, email):
        uuid = str(uuid4())

        #TODO: avoid duplicate signups
        if password != confirm_password:
            raise Exception("passwords do not match")
        
        password = password.encode() # encode pass before hashing
        salt = bcrypt.gensalt() # generates salt
        hashed_pass = bcrypt.hashpw(password,salt) # hashes password with salt

        _id = users.insert_one({
            "username":username, #TODO: make it as unique to avoid duplicate entries
            "password":hashed_pass,
            "registered_time":time(),
            "active": False,
            "activate_token": randint(10000,99999),
            "name":name,
            "email":email,
            "id":uuid
        })

        # TODO: send the otp (activate_token) to user thru email or sms  
        return uuid
    
    # returns the sessid of the Session object created while registering session
    @staticmethod
    def login(username, password):
        result = users.find_one({
            "username":username
        })

        if result:

            # #this method of checking pass is very insecure
            # if result['password'] == password: # alternate way: result.get('password') == password
            #     return True
            # else:
            #     #TODO: use sessions for additional security
            #     raise Exception("password is wrong")

            hashed_pass=result['password']
            
            if bcrypt.checkpw(password.encode(),hashed_pass):
                #TODO: register a session and return a session id on successful login
                '''
                register_session returns a Session object here with "id":"uuid"(uuid generated while registering session in db)
                '''
                sess = Session.register_session(username, request=request)

                return sess.id # sessid is returned to put it in flask's session object, so that it can be used to reconstruct session instance with this id and check for validity if authenticated is true
            else:
                #TODO: use sessions for additional security
                raise Exception("password is wrong")
        else:
            raise Exception("username is wrong")