from functools import wraps
from flask import jsonify, url_for
import datetime
from flask_login import current_user, login_required
import os
from flask_mail import Message
from app import db, mail
from app.models import Measure, MeasureRange, Notification
current_year = datetime.datetime.now().year
import google.generativeai as genai

API_KEY = os.environ.get('SECRET_KEY')
genai.configure(api_key= API_KEY)

model = genai.GenerativeModel(model_name= "gemini-1.5-flash")


def admin_required(fn):
  @wraps(fn)
  @login_required
  def wrapper(*args, **kwargs):
    user = current_user
    if not user or not user.is_admin:
      return jsonify({"message": "Admin access required"}), 403
    return fn(*args, **kwargs)
  return wrapper



def classify_result_value(measure_name, gender,value):
    # to avoid any error happened if gender doesn't exist assume its male
    if not gender:
      gender= "male"

    measure = Measure.query.filter_by(name= measure_name).first()
    if not measure:
       return None
    measure_range = MeasureRange.query.filter_by(measure_id= measure.id, gender= gender.capitalize()).first()
    # the gender is stored as "Male" or "female" so we use capitalize()
    if not measure_range:
       return None
    
    if value >= measure_range.lower and value <= measure_range.upper:
        return  "normal"
    else:
        return  "abnormal"
    


def parse_user_info(user):
   return f"gender:{user.gender}, birth year: {user.birth_year}, height: {user.height}, height: {user.height}, weight: {user.weight},smoke: {user.smoke}, num_of_pregnancies: {user.num_of_pregnancies}, is_pregnant: {user.is_pregnant}, exng: {user.exng}, heart_disease: {user.heart_disease}"


def generate_prompt(test_name, user_info, result, doctor_notes):
    return f"""Please interpret the results of the {test_name},
      test in a simplified way for a non-medical user,
      and limit the explanation to a maximum of 50 words.
      The user information is: {user_info}.\n     
      The test results are: {result}.
      Doctor’s notes: {doctor_notes}""".replace("\n      ","").replace("\n     ","")

def get_prompt_result(prompt):
  response = model.generate_content(prompt)
  return response.text


def trigger_notification(user_id, content):
  notification = Notification(user_id= user_id, content= content)
  db.session.add(notification)
  db.session.commit()
  


def send_reset_email(user):    
  token= user.get_reset_token()
  msg=Message('Password reset request', sender= os.environ.get('EMAIL_USER'),
               recipients= [user.email],
               body=f''' To reset your password, visit the following link:
               {url_for('auth.reset_password', token=token, _external=True)}  
                if you did not make this request, please ignore this email'''
              )
  mail.send(msg)


    
 
        
   














  

   