from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy() #instance #they all inherited from app at first and then it was changed
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()

login_manager.login_view = 'users.login' #telling the extension where the login route is located #this is basically for login_required to access something thingie
login_manager.login_message_category = 'info' #bootstrap class for decorating the message 'please log in to access this page'

def create_app(config_class=Config): #takes argument wrt what configuration object we wanna use for our application
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)    #inherit maadodikke change maadiddu bcos flask documentation tells me to do it like this
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users #importing all blueprints
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users) #registering those blueprints
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app