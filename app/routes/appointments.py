from flask import Blueprint, jsonify, render_template,request
from app import db
from app.models import Appointment, Lab, Test, User
from app.utils import doctor_required
from app.validators import validate_date
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('appointments', __name__, url_prefix='/appointments')


@bp.route("/appointments", methods=["GET"])
@login_required
def appointments():
   
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
@doctor_required
def schedule():
  try:
    data = request.get_json()
    user_id = data.get("user")   
    test_id = data.get("test")      
    lab_id = data.get("lab")
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
    
    if not validate_date(date):
      return jsonify({'message': 'Invalid date.'}), 400
            
      
    ex_appointment = Appointment.query.filter_by(date= date).first()
      
    if ex_appointment: 
      return jsonify({'message': 'Appointments already exist in this time.'}), 400

    appointment = Appointment(user_id= user_id, test_id= test_id, lab_id= lab_id, date= date)    
          
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment scheduled successfully!'}), 200
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': 'Database error occurred while schedule Appointment.'}), 500
    
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while schedule Appointment.'}), 500

   

'''
@bp.route("/available_periods", methods=["GET"])
@login_required
def periods():
    try:
        data = request.get_json()
        day = data.get("day") 
        lab_id = request.args.get("location")
        test_id = request.args.get("test") 

        if not day:
          return jsonify({'message': 'Day not found.'}), 400
        
      

        if not all([test_id, lab_id]):
            return render_template("error.jinja", message="All fields are required", code=400)

        test = Test.query.get(test_id)

        # Convert opening and closing times to datetime objects
        opening_time = datetime.strptime(f"{date} {OPENING_TIME}", "%Y-%m-%d %H:%M")
        closing_time = datetime.strptime(f"{date} {CLOSING_TIME}", "%Y-%m-%d %H:%M")

        # Get existing appointments for the day
        existing_appointments = (
        db.session.query(Appointment)
        .filter_by(test_id= test_id, lab_id= lab_id, is_done= 0)
        .filter(func.date(Appointment.time) == date)
        .all()
    )

        booked_periods = set(appointment.time for appointment in existing_appointments)
        available_periods = []
        current_time = opening_time
        time_slot = timedelta(minutes= test.duration)

        while current_time + time_slot <= closing_time:
            if current_time.strftime("%Y-%m-%d %H:%M") not in booked_periods:
                available_periods.append(current_time.strftime("%H:%M"))
            current_time += time_slot

        return render_template("appointments/periods.jinja", periods= available_periods)
    
    except Exception as e:
        return render_template("error.jinja",message=f"An unexpected error occurred.", code=500), 500
'''



@bp.route("/cancel_request", methods=["POST"])
@login_required
def cancel_request():
    try:
      data = request.get_json()
      appointment_id = data.get("id")
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
    



   
    
    
