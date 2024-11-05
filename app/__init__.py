from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()
admin = Admin( name='My Admin Panel', template_mode='bootstrap3')

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

@login_manager.unauthorized_handler
def handle_needs_login():
    if request.blueprint == 'admins':
        return redirect(url_for('admins.login')) # Redirect to admin login for admin routes
    return redirect(url_for('auth.login'))


def create_app():  
    app = Flask(__name__)
    # Load configuration
    app.config.from_object("config.Config")

    from app.routes.admins import MyAdminIndexView

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) 
    mail.init_app(app)  
    admin.init_app(app, index_view= MyAdminIndexView())

    from app.routes import auth, users,appointments, tests, notifications, admins

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(tests.bp)
    app.register_blueprint(notifications.bp)
    app.register_blueprint(admins.bp)


    from app.database import init_db
    
    with app.app_context():
    # Create the database if it doesn't exist
        db.create_all()
        init_db(db)
        
    return app
