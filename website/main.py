#Flask imports
from flask import Flask
from flask_wtf.csrf import CSRFProtect

#Blueprints
from api import api
from mysite import mysite

#Other imports
import os
import sys

csrf = CSRFProtect()

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(mysite)
app.secret_key = os.environ['FLASKKEY']

if __name__ == '__main__':
    csrf.init_app(app)
    
    if len(sys.argv) == 2:
        app.run(sys.argv[1])
    else:
        app.run()
