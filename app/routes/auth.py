from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User
from app.validators import validate_email, validate_fullname, validate_password
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")

        if not all([fullname, email, password]):
            return jsonify({'message': 'Missing fullname, email, or password'}), 400
        
        if not validate_fullname(fullname):
            return jsonify({'message': 'Invalid fullname'}), 400

        if not validate_email(email):
            return jsonify({'message': 'Invalid email format'}), 400
        
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            return jsonify({'message': password_message}), 400


        if User.query.filter_by(email = email).first():
            return jsonify({'message': 'User already exists'}), 400
        
        hashed_password = generate_password_hash(password)

        user = User(fullname= fullname, email= email, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully. Please check your email to activate your account.'}), 201
    

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while register the account'}), 500
     
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred while register the account'}), 500
    

@bp.route("/login", methods=["POST"])
def login():
    try:
        if current_user.is_authenticated:
          return jsonify({'message': 'User already logged in'}), 400  

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return jsonify({'message': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email = email).first()

        '''
        if user and not user.verified:
            return jsonify({'message': 'Email not verified'}), 400
        '''

        if user and check_password_hash(user.password, password):
            login_user(user) 
            return jsonify({'message': 'User login successfully'}), 200
            
        else:
            return jsonify({'message': 'Invalid email or password'}), 400
        
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error occurred while login the account'}), 500
    
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred while login the account'}), 500
        

@bp.route("/logout", methods=["POST"])
def logout():
  try:
    if not current_user.is_authenticated:
      return jsonify({'message': 'User already logged out'}), 400     

    logout_user()
    return jsonify({'message': 'User logout successfully'}), 200
    

  except SQLAlchemyError as e:
    return jsonify({'message': 'Database error occurred while logout the account'}), 500
                       
                       
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while logout the account'}), 500


    





