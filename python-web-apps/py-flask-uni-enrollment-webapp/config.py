import os

class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "secret_string_937cjabfkabfkakhbfihasf8ry9323rhn2"
    MONGODB_SETTINGS = {'db': 'Enrollment_Web_App_Db',
    'host' : 'mongodb://localhost:27017/Enrollment_Web_App_Db'
    }