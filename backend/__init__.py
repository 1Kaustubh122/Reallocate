from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta

from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ckjnveivibib98r7374cb3826482937649c264cb234c97Q37489723684796238796*(&^*&%SDSKNF%SDFSDF%&@#^*(&^(*@#)))'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servicehub.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Adjust as needed
app.config['SESSION_COOKIE_HTTPONLY'] = True


# app.config['SESSION_COOKIE_HTTPONLY'] = True

# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
socketio = SocketIO(app, cors_allowed_origins="*")  # Fixed typo: 'cros_allowed_orgins' to 'cors_allowed_origins'

db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)


loginManager = LoginManager(app)

from  backend import routes  # import models after db is initialized


