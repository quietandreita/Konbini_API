import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Itesz.123@localhost/Konbini'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
