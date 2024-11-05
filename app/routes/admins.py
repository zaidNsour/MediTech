from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from wtforms import PasswordField
from app import admin, db
from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.forms import LoginForm, NewUserForm
from app.models import QA, Appointment, Lab, Measure, Notification, Support, Test, User
from flask_admin.menu import MenuLink

bp = Blueprint('admins', __name__)


class MyModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
 
class MyAdminIndexView(AdminIndexView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin == True
  


################################################ routes ######################################


@bp.route("/login", methods=['GET', 'POST'])
def login():

  #if current_user.is_authenticated:
   # return redirect(url_for('admin.index')) 

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data ).first()
       
    if user and check_password_hash(user.password, form.password.data):
      login_user(user)
      return redirect(url_for('admin.index'))
    
    else:
      flash("Invalid email or password", "danger")
      flash_messages = get_flashed_messages() 
      return render_template("login.html", title="Login", form= form, flash_messages= flash_messages)
             
  flash_messages = get_flashed_messages() 
  return render_template("login.html", title="Login",
                           form = form, flash_messages= flash_messages)


@bp.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("admins.login"))

admin.add_link(MenuLink(name='Logout', category='', url="/logout"))


############################## User ################################
class UserAdmin(MyModelView):
  column_list = ['fullname','email','phone','insurance_num', 'gender', 'birth_year','height',
                  'weight','smoke', 'num_of_pregnancies', 'is_pregnant', 'exng', 'heart_disease',
                  'is_verified','is_admin']
  column_searchable_list = ['fullname', 'email']
  form_excluded_columns = ['password']
  page_size = 15
  form_extra_fields = { 'password2': PasswordField('Password'),}

  def create_form(self, obj=None): 
    return NewUserForm()
  
  def on_model_change(self, form, model, is_created):
    try:

      if form.password2.data != '':
        model.password = generate_password_hash(form.password2.data)
      
      
      if form.email.data != model.email:  # Email changed
       if self.model_class.query.filter_by(email = form.email.data).first():
        flash("Email already exists!", "error")
        return False  # Prevent saving
       
      return super().on_model_change(form, model, is_created)
    
    except Exception as e:
      flash(f"An error occurred while saving the model: {str(e)}", "error")


  def delete_model(self, model):
    try:
      self.session.delete(model)
      self.session.commit()
      flash('User was successfully deleted.', 'success')
      
    except Exception as e:
      flash(f'Error deleting user: {str(e)}', 'error')
      self.session.rollback()
      return False
    
    return True










admin.add_view(UserAdmin(User, db.session))
admin.add_view(MyModelView(Lab, db.session))
admin.add_view(MyModelView(Test, db.session))
admin.add_view(MyModelView(Measure, db.session))
admin.add_view(MyModelView(Appointment, db.session))
admin.add_view(MyModelView(Notification, db.session))
admin.add_view(MyModelView(Support, db.session))
admin.add_view(MyModelView(QA, db.session))
