from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

engine = None
Base = declarative_base()
db = SQLAlchemy()