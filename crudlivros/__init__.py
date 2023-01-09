from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '30cb1dc3e2111f40993bbdc307857c46'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

database = SQLAlchemy(app)
database.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'


from crudlivros import routes