import os



class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_DATABASE_URI = False

class LocalDevConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLITE_DB_DIR = os.path.abspath(os.path.join(basedir, "../", "instance"))
    print("Sqite database directory",SQLITE_DB_DIR)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR,"database.sqlite3")
    DEBUG = True