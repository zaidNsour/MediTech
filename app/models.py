from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  return User.query.get( int(user_id) )


class User(db.Model,UserMixin):
  #required info
  id = db.Column(db.Integer, primary_key=True)
  fullname = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False) 
  password = db.Column(db.String(120), nullable=False)
  is_verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default= False)
  is_doctor = db.Column(db.Boolean, nullable=False, default=False)

  #additional info 
  birth_year = db.Column(db.Integer, nullable=True) 
  # 1: male, 0: female
  gender = db.Column(db.Boolean, nullable=True)
  phone = db.Column(db.String(20), nullable=True)
  height = db.Column(db.Integer, nullable=True) 
  weight = db.Column(db.Integer, nullable=True)
  is_married = db.Column(db.Boolean, nullable=True)
  #(0: never worked, 1: private, 2: self-employed, 3: gov, 4: children)
  work = db.Column(db.Integer, nullable=True)
  # 0: rural, 1: urban
  residence = db.Column(db.Boolean, nullable=True)
  # 0: unknown, 1: never, 2: former, 3: current
  smoke = db.Column(db.Integer, nullable = True)
  num_of_pregnancies = db.Column(db.Integer, nullable = False, default= 0)
  is_pregnant = db.Column(db.Boolean, nullable = False, default = False)
  exng = db.Column(db.Boolean, nullable=True)
  heart_disease = db.Column(db.Boolean, nullable=True)
  insurance_num = db.Column(db.Integer, nullable=True) 

  appointments = db.relationship('Appointment', backref ='user', lazy=True)

  def __repr__(self):
     return f'User({self.id}, {self.fullname})'
  


class Lab(db.Model):
  id = db.Column(db.Integer, primary_key= True)
  name = db.Column(db.String(120), nullable= False)
  location = db.Column(db.Text, nullable= True)

  appointments = db.relationship('Appointment', backref ='lab', lazy=True)

  def __repr__(self):
     return f'Location({self.id}, {self.name})'
  


class Test(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  duration = db.Column(db.Integer, nullable=False) #in minutes
  name = db.Column(db.String(120), nullable=False)

  appointments = db.relationship('Appointment', backref ='test', lazy = True)
  preparation_steps = db.relationship('PreparationStep', backref ='test', lazy = True)
   # Many to Many rel with PreRequest through the TestPreRequest association table
  pre_requests = db.relationship('PreRequest', secondary='test_pre_request', backref='tests', lazy=True)

  def __repr__(self):
    return f'Test({self.id}, {self.name})'
  

class PreparationStep(db.Model):
  __tablename__ = 'preparation_step'
  id = db.Column(db.Integer, primary_key=True)
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
  description = db.Column(db.Text, nullable=False)
  number = db.Column(db.Integer, nullable=False)

  @staticmethod
  def add_step(test_id, description):    
     last_step = PreparationStep.query.filter_by(test_id= test_id).order_by(PreparationStep.number.desc()).first()
     next_number = 1 if last_step is None else last_step.number + 1   
     new_step = PreparationStep(test_id= test_id, number= next_number, description= description)
     db.session.add(new_step)
     db.session.commit()
     return new_step



class PreRequest(db.Model):
  __tablename__ = 'pre_request'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)  

  def __repr__(self):
    return f'PreRequest({self.id}, {self.name})'
  


# association table for prevent redundancy
class TestPreRequest(db.Model):
  __tablename__ = 'test_pre_request'
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key = True)
  pre_request_id = db.Column(db.Integer, db.ForeignKey('pre_request.id'), primary_key = True)

  # may need this references when use flask admin
  #test = db.relationship('Test', back_populates='pre_requests')
  #pre_request = db.relationship('PreRequest', back_populates='tests')


class Appointment(db.Model):
  id = db.Column(db.Integer, primary_key=True)   
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable= False)
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable= False)
  is_done = db.Column(db.Boolean, nullable= False, default= False)
  state = db.Column(db.String(60), nullable= True) 
 # if server clock different than local clock correct this by add or substract  
 # timedelta(hours = x)
  time = db.Column(db.String, nullable = True)                 
  creation_time= db.Column(db.DateTime, nullable= False, default= lambda: datetime.now())

  results = db.relationship('ResultField', backref= 'appointment', lazy= True)

  

class ResultField(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable= False)
  name = db.Column(db.String(180), nullable=False)  
  value = db.Column(db.String(180), nullable=False)  

  __table_args__ = (
        db.UniqueConstraint('appointment_id', 'name', name='unique_appointment_per_name'),
    )



class Notification(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  title = db.Column(db.String(100), nullable=False)  
  message = db.Column(db.Text, nullable= False, default= '')  



class Support(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), nullable = False )
  phone = db.Column(db.String(20), nullable=True)
  title = db.Column( db.String(80), nullable = False )
  description = db.Column(db.Text, nullable = True)




