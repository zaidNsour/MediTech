from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.utils import admin_required
from app.AI.classifier import classify
import datetime
from app.models import User, Appointment, ResultField
from app.forms.test_forms import DiabetsForm, HeartAttackForm, HeartFailureForm, StrokeForm
from sqlalchemy.exc import SQLAlchemyError

current_year = datetime.datetime.now().year
bp = Blueprint("admin", __name__)



@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
    try:
        appointment_id = request.args.get("id")
        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            flash("No appointment found with the given id")
            return redirect("/")

        test_type = appointment.test.name  

        if test_type == 'heart failure':
            form = HeartFailureForm()
        elif test_type == 'diabetes':
            form = DiabetsForm()
        elif test_type == 'stroke':
            form = StrokeForm()
        elif test_type == 'heart attack':
            form = HeartAttackForm()

        if form.validate_on_submit():
            for field_name, field_value in form.data.items():
                if field_name not in ['csrf_token', 'submit', 'classification']:
                    result = ResultField(
                        appointment_id= appointment_id,
                        name= field_name,
                        value= field_value,
                    )
                    db.session.add(result)

            appointment.is_done = True
            classify(appointment_id)
            db.session.commit()

            flash("Results recorded successfully!")
            return redirect(f"/result?id={appointment_id}")

        return render_template(f"admin/fill.jinja", form= form, id= appointment_id)
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return render_template("error.jinja", message="Result feilds already filled!", code= 400)



@bp.route("/user")
@admin_required
def user():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    return render_template("admin/user.jinja", user= user)


@bp.route("/users")
@admin_required
def users():
    users = User.query.all()[1:] # Assuming you're skipping the first user for some reason :)
    return render_template("admin/users.jinja", users=users, current_year=datetime.datetime.now().year)


@bp.route("/invert")
@admin_required
def invert():
    appointment_id = request.args.get("id")
    result_field = ResultField.query.filter_by(
        name= "classification", appointment_id= appointment_id
    ).first()
    result_field.value = str( 1 - int(result_field.value) )  # toggle between 0 and 1
    db.session.commit()
    return redirect(f"/result?id={appointment_id}")
