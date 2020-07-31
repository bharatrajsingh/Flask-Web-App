from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
db = SQLAlchemy(app)
login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from flaskblog.route import site_blueprint
app.register_blueprint(site_blueprint,url_prefix='/')
db.create_all()