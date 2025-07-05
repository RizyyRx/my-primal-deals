from mongogettersetter import MongoGetterSetter
from src.Database import Database
from time import time
from uuid import uuid4

db = Database.get_connection()

class SessionCollection(metaclass=MongoGetterSetter):
    def __init__(self,id):
        self._collection = db.sessions
        self._filter_query = {"id":id}

# when session object is created in register_session, it inherits the behavior defined by the metaclass MongoGetterSetter.
class Session:
    def __init__(self,id):
        self.id = id
        self.collection = SessionCollection(id) # self.collection will have the getter/setter functionality defined in MongoGetterSetter

    def is_valid(self):
        login_time = self.collection.time
        validity = self.collection.validity
        now = time()
        return now - login_time < validity
        # ifnow - login_time < validity
        #     return True
        # else:
        #     return False

    
    @staticmethod
    def register_session(username, request=None, validity=604800, _type="plain"):
        uuid = str(uuid4())
        collection = db.sessions

        """
        If user logs out, we set active to False and delete the session
        If user logs in, we set active to True and create a new session
        If user is inactive for 7 days, we discard the session, and discard active=True since validity expired

        Types:
        1. plain - Username and password used for authentication
        2. api - api Key used for authentication
        """

        if request is not None: #means flask's request object is sent when user logs in
            request_info = {
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'method': request.method,
                'url': request.url,
                'headers': dict(request.headers),
                'data': request.get_data().decode('utf-8')
            }
        else:
            request_info = None

        result = collection.insert_one({
            "id":uuid,
            "username":username,
            "time":time(),
            "validity":validity,
            "active":True,
            "type":_type,
            "request":request_info
        })

        return Session(uuid) #this will return a session instance with id to login func,

'''
A FLOW OF WHAT HAPPENS WHEN USER LOGS IN :

1. User submits login form with username and password.

2. auth() route in api.py is triggered.

3. Checks if session['authenticated'] is already True.
    If True and valid, returns "Already authenticated".
    If True but expired, sets session['authenticated'] = False and session in DB to inactive.

4. If not authenticated:
    Extracts username and password from the form.
    Calls User.login(username, password).

5. In User.login():
    Finds user by username in MongoDB.
    Verifies password with bcrypt.
    If correct, registers a new session using Session.register_session().

6. Session.register_session():
    Creates a new session in MongoDB with username, time, validity, etc.
    Returns session ID.

7. Back in auth():
    Sets session['authenticated'] = True, session['username'] = username, and session['sessid'] to session ID.
    Responds with a success message or redirects to the dashboard if requested.
'''