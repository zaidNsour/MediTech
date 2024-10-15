from functools import wraps
from flask import redirect, render_template, request
import datetime
from flask_login import current_user

from app.AI.ml_pipeline import diabetes_p, heart_attack, heart_failure
current_year = datetime.datetime.now().year
from app.AI.ml_pipeline  import stroke
from app.models import Appointment, ResultField, Test, User
from app import db


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect("/")
        return f(*args, **kwargs)
    
    return decorated_function


def snake_case_to_title_case(snake_str):
    return " ".join([word[0].upper() + word[1:] for word in snake_str.split("_")])


def on2positive(str):
    return "Positive" if str == "On" else str


def calculate_bmi(user):
    return user.weight / ((user.height / 100) ** 2)



  

   