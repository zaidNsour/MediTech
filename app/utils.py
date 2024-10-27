from functools import wraps
from flask import jsonify
import datetime
from flask_login import current_user, login_required
import os
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




def classify_result_value(test_name, measure_name, gender, value):
    # to avoid any error happened if gender doesn't exist assume its M
    if not gender:
      gender= "male"

    ranges = {
        "CBC test": {
            "Red blood cell count trillion cells/L": {"male": (4.35, 5.65), "female": (3.92, 5.13)},
            "Hemoglobin grams/dL": {"male": (13.2, 16.6), "female": (11.6, 15)},
            "Hematocrit % percent": {"male": (38.3, 48.6), "female": (35.5, 44.9)},
            "White blood cell count billion cells/L": {"male": (3.4, 9.6), "female": (3.4, 9.6)},
        },

        "glucose tolerance": {
            "glucose level mg/dL": {"male": (0, 140), "female": (0, 140)},
        },

        "Kidney Function test": {
            "Serum Creatinine mg/dL": {"male": (0.6, 1.2), "female": (0.5, 1.1)},
            "Blood Urea Nitrogen (BUN) mg/dL": {"male": (7, 20), "female": (7, 20)},
            "Glomerular Filtration Rate (GFR) mL/min/1.73 m²": {"male": (90, 120), "female": (90, 120)},
            "Urine Albumin-to-Creatinine Ratio (ACR) mg/g": {"male": (0, 30), "female": (0, 30)},
        },
        "Liver Function test": {
            "ALT U per liter": {"male": (7, 55), "female": (7, 55)},
            "AST U/L": {"male": (8, 48), "female": (8, 48)},
            "ALP U/L": {"male": (40, 129), "female": (40, 129)},
            "Albumin grams per deciliter (g/dL)": {"male": (3.5, 5.0), "female": (3.5, 5.0)},
            "Total protein milligrams per deciliter (mg/dL)": {"male": (6.3, 7.9), "female": (6.3, 7.9)},
            "GGT U/L": {"male": (8, 61), "female": (8, 61)},
            "LD U/L": {"male": (122, 222), "female": (122, 222)},
            "PT seconds": {"male": (9.4, 12.5), "female": (9.4, 12.5)},
        },
        "C-reactive protein (CRP)": {
            "CRP protein mg/L": {"male": (0, 2.0), "female": (0, 2.0)},
        },
        "thyroid-stimulating hormone (TSH) level": {
            "TSH level uIU/mL": {"male": (0.27, 4.2), "female": (0.27, 4.2)},
        },
        "Cholesterol test": {
            "Total cholesterol mg/dL": {"male": (0, 200), "female": (0, 200)},
        }
    }

    test_data = ranges.get(test_name)
    if test_data:
      measure = test_data.get(measure_name)
      if measure:
        range = measure.get(gender)
        if value >= range[0] and value <= range[1]:
            return  "normal"
        else:
            return  "abnormal"
        
    return  None


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














  

   