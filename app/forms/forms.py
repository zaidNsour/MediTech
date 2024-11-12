from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DateTimeField, DateTimeLocalField, IntegerField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,NumberRange
from wtforms.validators import Regexp, EqualTo, ValidationError, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Lab, Measure, Test, User


def choice_query_test():
  return Test.query 

def choice_query_lab():
  return Lab.query 

def choice_query_user():
  return User.query 



class ResetPasswordForm(FlaskForm):
  password=PasswordField(
      "password",
      validators=[ DataRequired(),Regexp("^(?=.*[A-Z])(?=.*[!@#$%^&*_\-()]).{8,30}$")]
    )
  confirm_password=PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")] )
  submit=SubmitField("Reset password")


class LoginForm(FlaskForm):
  email=StringField("Email", validators=[DataRequired(), Email()]  )
  password=PasswordField("Password", validators=[DataRequired()])
  submit=SubmitField("Login")


######################### Admin dashboard forms  #################################


class NewUserForm(FlaskForm):
  fullname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField("Email", validators=[DataRequired(), Email()] )
  password2 = PasswordField(
      "password",
      validators=[ 
        DataRequired(),
        Regexp(
          "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{8,32}$"
          )
       ]
    )
  phone = StringField("Phone", validators=[DataRequired(), Length(min=8, max=15)])
  insurance_num = StringField("Insurance number", validators=[DataRequired(), Length(min=8, max=15)])
  gender = SelectField(
    "Gender",
    choices=[('male', 'Male'), ('female', 'Female')],
    validators=[DataRequired()]
  )
  birth_year = IntegerField("Birth Year",validators=[DataRequired(), NumberRange(min=1900, max=2023)])
  height = IntegerField("Height",validators=[DataRequired(), NumberRange(min=10, max=500)])
  weight = IntegerField("Weight",validators=[DataRequired(), NumberRange(min=10, max=500)])
  smoke = SelectField(
    "Smoke",
    choices=[('unknown','unknown'),('never','never'),('former','former'),('current','current')],
    validators=[DataRequired()]
  ) 
  num_of_pregnancies= IntegerField("Num Of Pregnancies",
                                   validators=[ NumberRange(min=0, max=30)])
  is_pregnant = BooleanField("Is Pregnant")
  exng = BooleanField("Exng")
  heart_disease = BooleanField("Heart Disease")

  is_verified = BooleanField("Is Verified")
  is_admin = BooleanField("Is Admin")

  def validate_email(self, email):
    user=User.query.filter_by(email= email.data).first()
    if user:
      raise ValidationError("Email is already exist")
    
class NewMeasureForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Length(min=4)])
  test = QuerySelectField("Test name", query_factory= choice_query_test, get_label="name")
 
  def validate_name(self, name):
    measure = Measure.query.filter_by(name= name.data).first()
    if measure:
      raise ValidationError("Measure is already exist")


class UpdateMeasureForm:
  name = StringField("Name", validators=[DataRequired(), Length(min= 4)])



class NewAppointmentForm(FlaskForm):
  lab = QuerySelectField("Lab Name", query_factory= choice_query_lab, get_label="name")
  test = QuerySelectField("Test Name", query_factory= choice_query_test, get_label="name")
  user = QuerySelectField("User ID", query_factory= choice_query_user, get_label="id")
  date = DateTimeLocalField(
        'Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
  doctor_notes = StringField("Doctor notes", validators=[DataRequired(), Length(min= 6)])
 
 
class UpdateAppointmentForm(FlaskForm):
  lab = QuerySelectField("Lab Name", query_factory= choice_query_lab, get_label="name")
  test = QuerySelectField("Test Name", query_factory= choice_query_test, get_label="name")
  date = DateTimeLocalField(
        'Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
  is_done= BooleanField("Is Done")

  state = SelectField( 
    "State",
    choices=[('Scheduled','Scheduled'),('Confirmed','Confirmed'),
             ('Canceled','Canceled'),('Cancellation Requested','Cancellation Requested')],
    validators=[DataRequired()]
  ) 
  
  doctor_notes = StringField("Doctor notes", validators=[DataRequired(), Length(min= 6)])

