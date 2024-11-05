from flask import Blueprint, jsonify, request
from app.models import QA, Appointment, Lab, Support, Test, User
from app.utils import admin_required
from app.validators import validate_email, validate_exng, validate_fullname, validate_heart_disease
from app.validators import validate_height, validate_insurance_num, validate_is_pregnant
from app.validators import  validate_num_of_pregnancies, validate_smoke, validate_weight, validate_phone

from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app import db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/users', methods=['GET'])
@admin_required
def info():
  users = User.query.all()
  users_list= [user.to_dict() for user in users]
  return jsonify({"users": users_list}), 200


@bp.route('/all_info', methods=['GET'])
@login_required
def all_info():
  try:
    user = User.query.filter_by(id= current_user.id).first()
    if user:
      return jsonify(user.to_dict()), 200 
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while fetch the user info'}), 500

@bp.route("/update_profile_info", methods=["PUT"])
@login_required
def update_profile_info():
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

    if phone:
      if not validate_phone(phone):
        return jsonify({'message': 'Invalid phone'}), 400
      user.phone = phone

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
    return jsonify({'message': f'An error occurred while update the user info{e}'}), 500


@bp.route("/update_medical_info", methods=["PUT"])
@admin_required
def update_medical_info():
  try:
    data = request.get_json()
    user_id = data.get("user_id")
    height= data.get('height')
    weight= data.get('weight')
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
      user.weight = weight

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
     
      user.is_pregnant= is_pregnant
     
    if exng:
      if not validate_exng(exng):
        return jsonify({'message': 'Invalid exng'}), 400
     
      user.exng = exng
     
    if heart_disease:
      if not validate_heart_disease(heart_disease):
        return jsonify({'message': 'Invalid heart_disease'}), 400
  
      user.heart_disease = heart_disease
     

    db.session.commit()
    return jsonify({'message': 'User Profile updated successfully.'}), 200

  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while update the user info'}), 500
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while update the user info'}), 500
  

@bp.route('/support', methods = ['POST'])
@login_required
def support():
  try:
    user_id = current_user.id

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not all([ title, description]):
        return jsonify({'message': 'Missing title or description'}), 400
    
    support = Support(user_id= user_id, title= title, description= description)
    db.session.add(support)
    db.session.commit()

    return jsonify({"message": "support created successfully."}), 201

  except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error occurred while adding the support'}), 500
  
    
  except Exception as e:
        return jsonify({'message': 'An error occurred while adding the support'}), 500
  


@bp.route('/faq', methods = ['GET'])
@login_required
def faq():
  try:
    qas = QA.query.all()
    qas_list = [qa.to_dict() for qa in qas]
    return jsonify({"faq": qas_list}), 200
  
  except Exception as e:
    return jsonify({'message': 'An error occurred while fetching the faq'}), 500