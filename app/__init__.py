from flask import Flask
from config import Config
from flask_login import LoginManager #to log users in and out and maintain the session
from flask_sqlalchemy import SQLAlchemy #this talks to the database
from flask_migrate import Migrate #this makes altering the db a lot easier



# init login manager
login = LoginManager()
# this is where you will be sent if you are not logged in
login.login_view = 'auth.login'

# stuff to work with the db

# initializes the database
db = SQLAlchemy()

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)       # constructor
    app.config.from_object(config_class)
    #register plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register our blueprints with the app
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.main import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app