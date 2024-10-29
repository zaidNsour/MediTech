from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    # Load configuration
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) 
    mail.init_app(app)  

    from app.routes import auth, users,appointments, tests, notifications

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(tests.bp)
    app.register_blueprint(notifications.bp)


    from app.database import init_db
    
    with app.app_context():
    # Create the database if it doesn't exist
        db.create_all()
        init_db(db)
        
    return app
