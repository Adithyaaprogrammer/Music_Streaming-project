import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from application.configure import LocalDevConfig
from application.database import db
from application import models



app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.controllers import *

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080)