from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,NumberRange
from wtforms.validators import Regexp, EqualTo, ValidationError, Length

from app.models import User






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

