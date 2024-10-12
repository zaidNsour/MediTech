from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.utils import admin_required, classify
import datetime
from app.models import User, Appointment, ResultField
from app.forms.test_forms import DiabetsForm, HeartAttackForm, HeartFailureForm, StrokeForm
current_year = datetime.datetime.now().year
bp = Blueprint("admin", __name__)


'''

@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
    appointment_id = request.args.get("id")
    form = HeartFailureForm()

    if request.method == "GET":
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            test_type = appointment.test.name
            return render_template(f"admin/tests/{test_type}.jinja", id=appointment_id)
        else:
            flash("No test found for the given appointment ID")
            return redirect("/")

    # Validate form data to check if all fields are present
    missing_fields = []
    for field_name, field_value in request.form.items():
        if not field_value:
            missing_fields.append(field_name)
        
        # If no missing fields, add result to the database
        result = ResultField(
            appointment_id=appointment_id,
            name=field_name,
            value=field_value,
        )
        db.session.add(result)

    if missing_fields:
        # Show error message if any required field is missing
        flash(f"Missing fields: {', '.join(missing_fields)}. Please fill in all required fields.", "error")
        return redirect(f"/fill?id={appointment_id}")

    # Mark appointment as done
    appointment = Appointment.query.get(appointment_id)
    appointment.is_done = True

    # Call classification function (assuming this is a prediction-related task)
    classify(appointment_id)

    # Commit the session to save changes to the DB
    db.session.commit()

    flash("Results recorded successfully!")
    return redirect(f"/result?id={appointment_id}")

'''




@bp.route("/fill", methods=["GET", "POST"])
@admin_required
def fill():
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
            if field_name not in ['csrf_token', 'submit']:
                result = ResultField(
                    appointment_id=appointment_id,
                    name=field_name,
                    value=field_value,
                )
                db.session.add(result)

        appointment.is_done = True
        classify(appointment_id)
        db.session.commit()

        flash("Results recorded successfully!")
        return redirect(f"/result?id={appointment_id}")

    return render_template(f"admin/fill.jinja", form= form, id= appointment_id)



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
