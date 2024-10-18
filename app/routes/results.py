from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app import db
from app.models import Appointment, ResultField

bp = Blueprint("results", __name__)


@bp.route("/results")
@login_required
def results():

    if current_user.is_admin:
        appointments = Appointment.query.filter_by(is_done = True).all()    
    else:
        appointments = Appointment.query.filter_by(is_done = True, user_id = current_user.id).all()    
         

    return render_template(("admin" if current_user.is_admin else "results") + "/results.jinja",
                           appointments = appointments )


@bp.route("/result")
@login_required
def result():
    appointment_id = request.args.get("id")

     # we need use join in case like that
    query = db.session.query(ResultField).join(Appointment, ResultField. appointment_id == Appointment.id)

    if current_user.is_admin:
        result_fields = query.filter(ResultField.appointment_id == appointment_id).all()
    else:
        # filter used here to combine conditions from different models
        result_fields = query.filter( ResultField.appointment_id == appointment_id, 
                               Appointment.user_id == current_user.id).all()
        

    
    for i in range(len(result_fields)):
        if result_fields[i].name == 'classification':
                classification = render_template(f"results/{"" if result_fields[i].value == '0' else "ab"}normal.jinja")
                result_fields.remove(result_fields[i])
                break     
       
  
    return render_template(
        "results/result.jinja", result_fields= result_fields,
          classification= classification, id= appointment_id, user= current_user
    )