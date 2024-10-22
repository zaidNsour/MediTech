from flask import Blueprint, jsonify,request
from app import db
from app.models import Appointment, Measure, ResultField, Test
from app.utils import admin_required
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.validators import validate_measures_value


bp = Blueprint('tests', __name__, url_prefix='/tests')

@bp.route("/fill", methods=["POST"])
@admin_required
def fill():
  try:  
    data = request.get_json()
    appointment_id = data.get("appointment_id")
    values = data.get("values")

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
      return jsonify({"message": "No appointment found with the given id."}), 400
        
    test = appointment.test
    measures = test.measures
    if len(values) < len(measures):
      return jsonify({"message": "There is missing measures value."}), 400 


    for measure_name, value in values.items():
      measure = Measure.query.filter_by(test_id= test.id, name= measure_name).first()
      if not measure:
        return jsonify({"message": "Invalid measures for this test."}), 400
      if not validate_measures_value(measure.id, value):
        return jsonify({"message": f"Invalid values for the given measure: {measure_name}"}), 400
      
      result = ResultField(appointment_id= appointment_id, measure_id= measure.id, value= value)
      db.session.add(result)

    appointment.is_done = True
    db.session.commit()
    return jsonify({'message': 'Results recorded successfully!'}), 201 
       
    
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while fill the test.'}), 500
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fill the test.'}), 500
 


@bp.route("/results")
@login_required
def results():
  try:
    if current_user.is_admin:
      appointments = Appointment.query.filter_by(is_done = True).all()    
    else:
      appointments = Appointment.query.filter_by(is_done = True, user_id = current_user.id).all()  
          
    results_list = [{"appointment_id":appointment.id,
                    "user_id":appointment.user.id,
                    "fullname":appointment.user.fullname,
                    "test":appointment.test.name,
                    "lab":appointment.lab.name,
                    "date":appointment.date,
                    "creation_date":appointment.creation_date
                    } for appointment in appointments ]
      
    return jsonify({"results": results_list}), 200
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the results.'}), 500


@bp.route("/result")
@login_required
def result():
  try:
    data = request.get_json()
    appointment_id = data.get("appointment_id")
      
    if current_user.is_admin:
      appointment = Appointment.query.filter_by(id= appointment_id, is_done= True)     
    else:
      appointment = Appointment.query.filter_by(id= appointment_id, user_id= current_user.id, is_done= True)  

    if not appointment:
      return jsonify({"message": "Invalid appointment ID."}), 400 

    result_fields = ResultField.query.filter_by(appointment_id= appointment_id).all()
    result_list = [ {"name": result.measure.name, "value":result.value}
                    for result in result_fields ]
    
    return jsonify({"result_fields": result_list, "doctor_notes": appointment.doctor_notes}), 200
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the result.'}), 500


    
@bp.route("/tests")
@login_required
def tests():
  try:
    tests = Test.query.all()   
    tests_list = [{"id":test.id, "name":test.name} for test in tests] 
    return jsonify({"tests": tests_list}), 200
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the tests.'}), 500


@bp.route("/test")
@login_required
def test():
  try:
    data = request.get_json()
    test_id = data.get("test_id")
    test = Test.query.get(test_id)
    if not test:
      return jsonify({"message": "Invalid test ID."}), 400 
      
    return jsonify({"test": test.to_dict()}), 200
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the test.'}), 500
      
         
