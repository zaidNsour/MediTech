
from flask import  render_template, request
import datetime
from app.AI.ml_pipeline import diabetes_p, heart_attack, heart_failure, stroke
from app.utils import calculate_bmi
current_year = datetime.datetime.now().year
from app.models import Appointment, ResultField, Test, User
from app import db



def classify(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user = User.query.get(appointment.user_id)
    test = Test.query.get(appointment.test_id)
    test_type = test.name

    if test_type == "stroke":
      prediction = stroke_classify(user)
        
    elif test_type == "heart attack":
      prediction = heart_attack_classify(user)

    elif test_type == "diabetes":
      prediction = diabets_classify(user)

    elif test_type == "heart failure":
      prediction = heart_failure_classify(user)

    # Insert the prediction result into the ResultField table
    result = ResultField(
        appointment_id= appointment_id,
        name= "classification",
        value= str(prediction)
    )
   
    db.session.add(result)
    # if u want use this method dont forget to commit the changes


  
def diabets_classify(user):
  glucose = request.form.get("glucose")
  blood_pressure = request.form.get("blood_pressure")
  skin_thickness = request.form.get("skin_thickness")
  insulin = request.form.get("insulin")
  pedigree = request.form.get("pedigree")

  if not all([glucose, blood_pressure,skin_thickness,insulin,pedigree]):
    return render_template("error.jinja", message="All fields are required", code=400)

  data = [
            user.num_of_pregnancies, 
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            calculate_bmi(user),
            pedigree,
            current_year - user.birth_year,
        ]
  return diabetes_p.predict(data)


def heart_attack_classify(user):
  chest_pain = request.form.get("chest_pain")
  blood_pressure = request.form.get("blood_pressure")
  cholesterol = request.form.get("cholesterol")
  fasting_blood_sugar = request.form.get("fasting_blood_sugar")
  resting_ECG = request.form.get("resting_ECG")
  max_heart_rate = request.form.get("max_heart_rate")
  oldpeak = request.form.get("oldpeak")
  slope = request.form.get("slope")

  if not all([chest_pain, blood_pressure,cholesterol,fasting_blood_sugar,resting_ECG,
                    max_heart_rate,oldpeak,slope]):
    return render_template("error.jinja", message="All fields are required", code=400)

  data = [
            current_year - user.birth_year,
            "M" if user.gender == 1 else "F",
            chest_pain,
            blood_pressure,
            cholesterol,
            1 if int(fasting_blood_sugar) > 120 else 0,
            resting_ECG ,
            max_heart_rate,
            "Y" if user.exng == 1 else "N",
            oldpeak,
            slope,
        ]
  
  return heart_attack.predict(data)



def heart_failure_classify(user):
  anaemia = request.form.get("anaemia", "0")
  creatinine_phosphokinase = request.form.get("creatinine_phosphokinase")
  diabetes = request.form.get("diabetes", "0")
  ejection_fraction = request.form.get("ejection_fraction")
  high_blood_pressure = request.form.get("high_blood_pressure", "0")
  platelets = request.form.get("platelets")
  serum_creatinine = request.form.get("serum_creatinine")
  serum_sodium = request.form.get("serum_sodium")

  if not all([anaemia,creatinine_phosphokinase,diabetes,ejection_fraction,high_blood_pressure,
                    platelets,serum_creatinine,serum_sodium]):
    return render_template("error.jinja", message="All fields are required", code=400)

  data = [
            current_year - user.birth_year,
            1 if anaemia == "1" else 0,
            creatinine_phosphokinase,
            1 if diabetes == "1" else 0,
            ejection_fraction,
            1 if high_blood_pressure  == "1" else 0,
            platelets,
            serum_creatinine,
            serum_sodium,
            user.gender,
            1 if user.smoke == 3 else 0,
            250,  # Assuming this is a fixed value  
        ]
  
  return heart_failure.predict(data)


def stroke_classify(user):
  glucose = request.form.get("glucose")
  hypertension = request.form.get("hypertension", "off")

  if not all([glucose, hypertension]):
    return render_template("error.jinja", message="All fields are required", code=400)

  data = [
            user.gender,
            current_year - user.birth_year,
            1 if hypertension == "on" else 0,
            user.heart_disease,
            user.work,
            glucose,
            calculate_bmi(user),
        ]
  
  return  stroke.predict(data)


  