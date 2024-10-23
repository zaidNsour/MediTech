from functools import wraps
from flask import jsonify
import datetime
from flask_login import current_user, login_required

current_year = datetime.datetime.now().year


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
      gender= "M"

    ranges = {
        "CBC test": {
            "Red blood cell count trillion cells/L": {"M": (4.35, 5.65), "F": (3.92, 5.13)},
            "Hemoglobin grams/dL": {"M": (13.2, 16.6), "F": (11.6, 15)},
            "Hematocrit % percent": {"M": (38.3, 48.6), "F": (35.5, 44.9)},
            "White blood cell count billion cells/L": {"M": (3.4, 9.6), "F": (3.4, 9.6)},
        },

        "glucose tolerance": {
            "glucose level mg/dL": {"M": (0, 140), "F": (0, 140)},
        },

        "Kidney Function test": {
            "Serum Creatinine mg/dL": {"M": (0.6, 1.2), "F": (0.5, 1.1)},
            "Blood Urea Nitrogen (BUN) mg/dL": {"M": (7, 20), "F": (7, 20)},
            "Glomerular Filtration Rate (GFR) mL/min/1.73 m²": {"M": (90, 120), "F": (90, 120)},
            "Urine Albumin-to-Creatinine Ratio (ACR) mg/g": {"M": (0, 30), "F": (0, 30)},
        },
        "Liver Function test": {
            "ALT U per liter": {"M": (7, 55), "F": (7, 55)},
            "AST U/L": {"M": (8, 48), "F": (8, 48)},
            "ALP U/L": {"M": (40, 129), "F": (40, 129)},
            "Albumin grams per deciliter (g/dL)": {"M": (3.5, 5.0), "F": (3.5, 5.0)},
            "Total protein milligrams per deciliter (mg/dL)": {"M": (6.3, 7.9), "F": (6.3, 7.9)},
            "GGT U/L": {"M": (8, 61), "F": (8, 61)},
            "LD U/L": {"M": (122, 222), "F": (122, 222)},
            "PT seconds": {"M": (9.4, 12.5), "F": (9.4, 12.5)},
        },
        "C-reactive protein (CRP)": {
            "CRP protein mg/L": {"M": (0, 2.0), "F": (0, 2.0)},
        },
        "thyroid-stimulating hormone (TSH) level": {
            "TSH level uIU/mL": {"M": (0.27, 4.2), "F": (0.27, 4.2)},
        },
        "Cholesterol test": {
            "Total cholesterol mg/dL": {"M": (0, 200), "F": (0, 200)},
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
        
    return  "Test or measure not found"










  

   