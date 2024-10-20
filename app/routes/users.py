from flask import Blueprint, jsonify, request
from app.models import Appointment, Lab, Test, User
from app.utils import admin_required, doctor_required
from app.validators import validate_email, validate_exng, validate_fullname, validate_heart_disease
from app.validators import validate_height, validate_insurance_num, validate_is_pregnant
from app.validators import  validate_num_of_pregnancies, validate_smoke, validate_weight
from config import OPENING_TIME, CLOSING_TIME 
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/users', methods=['GET'])
@admin_required()
def info():
  users = User.query.all
  users_list= [user.to_dict for user in users]
  return jsonify({"users": users_list}), 200


@bp.route('/info', methods=['GET'])
@login_required()
def info():
  user = User.query.filter_by(id= current_user.id).first()
  if user:
    return jsonify(user.to_dict()), 200 


@bp.route("/update_profile_info", methods=["PUT"])
@login_required()
def update_info():
  try:
    
    data = request.get_json()
    
    fullname= data.get('fullname')
    email= data.get('email')
    phone = data.get('phone')
    insurance_num = data.get('insurance_num')

    user = current_user

    if fullname:
      if not validate_fullname(fullname):
        return jsonify({'message': 'Invalid fullname'}), 400
      user.fullname = fullname

    if email:
      if not validate_email(email):
        return jsonify({'message': 'Invalid email'}), 400
      user.email = email

    if insurance_num:
      if not validate_insurance_num(insurance_num):
        return jsonify({'message': 'Invalid insurance number'}), 400
      user.insurance_num = insurance_num

    db.session.commit()
    return jsonify({'message': 'User Profile updated successfully.'}), 200

  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while update the user info'}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while update the user info'}), 500


@bp.route("/update_medical_info", methods=["PUT"])
@doctor_required()
def update_info():
  try:

    data = request.get_json()

    user_id = data.get("id")
    height= data.get('height')
    weight= data.get('height')
    smoke = data.get('smoke')
    num_of_pregnancies = data.get('num_of_pregnancies')
    is_pregnant = data.get('is_pregnant')
    exng = data.get('exng')
    heart_disease = data.get('heart_disease')
    
    if not user_id:
      return jsonify({'message': 'Missing user ID'}), 400

    user = User.query.filter_by(id = user_id).first()

    if not user:
      return jsonify({'message': 'Invalid user ID'}), 400

    if height:
      if not validate_height(height):
        return jsonify({'message': 'Invalid height'}), 400
      user.height = height

    if weight:
      if not validate_weight(weight):
        return jsonify({'message': 'Invalid weight'}), 400
      user.weight = height

    if smoke:
      if not validate_smoke(smoke):
        return jsonify({'message': 'Invalid Smoke stauts'}), 400
      user.smoke = smoke

    if num_of_pregnancies:
      if not validate_num_of_pregnancies(num_of_pregnancies):
        return jsonify({'message': 'Invalid num of pregnancies'}), 400
      user.num_of_pregnancies = num_of_pregnancies

    if is_pregnant:
      if not validate_is_pregnant(is_pregnant):
        return jsonify({'message': 'Invalid pregnant status'}), 400
      if is_pregnant == 1:
        user.is_pregnant= True
      else:
        user.is_pregnant= False

    if exng:
      if not validate_exng(exng):
        return jsonify({'message': 'Invalid exng'}), 400
      if exng == 1:
        user.exng = True
      else:
        user.exng = False

    if heart_disease:
      if not validate_heart_disease(heart_disease):
        return jsonify({'message': 'Invalid heart_disease'}), 400
      if heart_disease == 1:
        user.heart_disease = True
      else:
        user.heart_disease = False


    db.session.commit()
    return jsonify({'message': 'User Profile updated successfully.'}), 200

  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while update the user info'}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while update the user info'}), 500