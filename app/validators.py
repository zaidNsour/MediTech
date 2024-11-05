import re

def is_boolean(num):
  return num in [True,False]

def validate_fullname(fullname):
    return len(fullname) >= 3

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(value):
    if not value:
        return False, 'Please enter your password'
    elif len(value) < 8:
        return False,'Password must be at least 8 characters'
    elif not re.search(r'[A-Z]', value):
        return False,'Password must contain at least one uppercase letter'
    elif not re.search(r'[0-9]', value):
        return False,'Password must contain at least one number'
    elif not re.search(r'[_!@#$%^&*(),.?":{}|<>]', value):
        return False,'Password must contain at least one special character'
    return True, ""

def validate_phone(phone):
    return 8 <= len(phone) <= 15

def validate_height(height):
    return height > 0 and height < 600

def validate_weight(weight):
    return weight > 0 and weight < 400

def validate_smoke(smoke):
    return smoke in ["unknown","never","former","current"]

def validate_num_of_pregnancies(num_of_pregnancies):
    return num_of_pregnancies >= 0 and num_of_pregnancies <= 50

def validate_is_pregnant(is_pregnant):
    return is_boolean(is_pregnant)

def validate_exng(exng):
    return is_boolean(exng)

def validate_heart_disease(heart_disease):
    return is_boolean(heart_disease)

def validate_date(date):
  return True

def validate_insurance_num(insurance_num):
   return 8 <= len(insurance_num) <= 15


def validate_measures_value(measure_id, value):
  return True    


def validate_content(content):
    return len(content) >= 8