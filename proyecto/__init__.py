#__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#control de loggeo de usuarios
login_manager = LoginManager()

app = Flask(__name__)
#app configurations
app.config['SECRET_KEY'] = 'E0^zF_o{J*+GH&BYM}_3]D65h@WUV7TV=l0=1Y`vPSwYX+`{.U7+8#9;wS^T2V@F'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/cafeteria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#database
db = SQLAlchemy(app)
Migrate(app,db) #migrar db

#iniciar pág de loggeo
login_manager.init_app(app)
login_manager.login_view = 'inicio'






