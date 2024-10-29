from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email
from wtforms.validators import Regexp, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import Regexp, ValidationError, EqualTo





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

