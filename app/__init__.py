from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


# import all of the routes from the routes file into the current package
from app import routes
# or from . import routes