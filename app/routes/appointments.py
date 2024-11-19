from flask import Blueprint, jsonify, request
from app import db
from app.models import Appointment, Lab, Test, User
from app.utils import admin_required
from app.validators import validate_date, validate_day
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from config import OPENING_TIME, CLOSING_TIME

bp = Blueprint('appointments', __name__, url_prefix='/appointments')


@bp.route("/appointments", methods=["GET"])
@login_required
def appointments():
  if current_user.is_admin:
    appointments = Appointment.query.filter_by(is_done = False) 
  else:
    appointments = Appointment.query.filter_by(is_done = False, user_id = current_user.id)   
  appointments_list = [appointment.to_dict() for appointment in appointments]
  return jsonify({"appointments": appointments_list}), 200
  
'''
{
  "user": 1
  "test": 1,
  "location": 2,
  "date": "2024-10-18T15:30:00"
}
'''

@bp.route("/schedule", methods=[ "POST"])
@admin_required
def schedule():
  try:
    data = request.get_json()
    user_id = data.get("user_id")   
    test_id = data.get("test_id")      
    lab_id = data.get("lab_id")
    date = data.get("date")  
      
    if not all([user_id, test_id, lab_id, date]):
      return jsonify({'message': 'All fields are required'}), 400 
    
    user = User.query.get(user_id)
    test = Test.query.get( test_id )   
    lab = Lab.query.get( lab_id )

    if not user:
      return jsonify({'message': 'User not found.'}), 400     
    
    if not test:
      return jsonify({'message': 'Test not found.'}), 400
    
    if not lab:
      return jsonify({'message': 'Lab not found.'}), 400
    
    is_valid_date, date_message = validate_date(date)
    if not is_valid_date:
      return jsonify({'message': date_message}), 400
    
    date_object = datetime.fromisoformat(date)

  
    ex_appointment = Appointment.query.filter_by(date= date_object, lab_id= lab_id).first()
      
    if ex_appointment: 
      return jsonify({'message': 'Appointments already exist in this time.'}), 400

    appointment = Appointment(user_id= user_id, test_id= test_id, lab_id= lab_id, date= date_object)    
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment scheduled successfully!'}), 200
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': f'Database error occurred while schedule Appointment.'}), 500
    
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while schedule Appointment.'}), 500

   


@bp.route("/available_periods", methods=["GET"])
@admin_required
def periods():
    try:
        data = request.get_json()
        day = data.get("day") 
        lab_id = data.get("lab_id")
        test_id = data.get("test_id") 

        if not all( [test_id, lab_id, day] ):
          return jsonify({'message': 'Missing day, lab id, or test id.'}), 400
        
        test = Test.query.get(test_id)
        lab = Lab.query.get( lab_id )

        if not test:
          return jsonify({'message': 'Test not found.'}), 400
    
        if not lab:
          return jsonify({'message': 'Lab not found.'}), 400
        
        try:
            date_object = datetime.fromisoformat(day)
        except ValueError:
            return jsonify({'message': 'Invalid day format.'}), 400


        # Get existing appointments for the day
        existing_appointments = Appointment.get_appointments_for_day(date_object)
        booked_periods = set(appointment.date.time() for appointment in existing_appointments)

       
        opening_time = datetime.strptime(OPENING_TIME,"%H:%M").time()
        closing_time = datetime.strptime(CLOSING_TIME,"%H:%M").time()
        
        current_time = datetime.combine(date_object, opening_time)
        end_time = datetime.combine(date_object, closing_time)
        time_slot = timedelta(minutes= test.duration)

        available_periods = []
        while current_time + time_slot <= end_time:
            if current_time.time() not in booked_periods:
                available_periods.append(current_time.strftime("%H:%M"))
            current_time += time_slot

        return jsonify({'available_periods': available_periods}), 200
    
    except Exception as e:
        return jsonify({'An unexpected error occurred while fetching the available periods.'}), 500
        


@bp.route("/cancel_request", methods=["POST"])
@login_required
def cancel_request():
    try:
      data = request.get_json()
      appointment_id = data.get("appointment_id")
      appointment = Appointment.query.filter_by(id = appointment_id, user_id = current_user.id).first()

      if not appointment:
        return jsonify({'message': 'Invalid Appointment.'}), 400      

      appointment.state = "Cancellation Requested"
      db.session.commit()
      return jsonify({'message': 'Cancellation Requested successfully!'}), 201 
    
    except SQLAlchemyError as e:
      db.session.rollback()
      return jsonify({'message': 'Database error occurred while Cancellation Requested.'}), 500
    
    except Exception as e:
      return jsonify({'message': 'An unexpected error occurred while Cancellation Requested.'}), 500
    


@bp.route("/labs")
@login_required
def labs():
  try:
    labs = Lab.query.all()   
    labs_list = [lab.to_dict() for lab in labs] 
    return jsonify({"labs": labs_list}), 200
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the labs.'}), 500
    



   
    
    
