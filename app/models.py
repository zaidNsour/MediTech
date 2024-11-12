from itsdangerous import Serializer
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
  return User.query.get( int(user_id) )



class User(db.Model, UserMixin):
  # profile info
  id = db.Column(db.Integer, primary_key=True)
  fullname = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False) 
  password = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(20), nullable=True)
  is_verified = db.Column(db.Boolean, nullable=False, default=False)
  is_admin = db.Column(db.Boolean, nullable=False, default= False)
  insurance_num = db.Column(db.String(20), nullable=True) 

  #medical info
  gender = db.Column(db.String(10), nullable=True)
  birth_year = db.Column(db.Integer, nullable=True) 
  height = db.Column(db.Integer, nullable=True) 
  weight = db.Column(db.Integer, nullable=True)
  # unknown,never,former,current
  smoke = db.Column(db.String(20), nullable = True)
  num_of_pregnancies = db.Column(db.Integer, nullable = False, default= 0)
  is_pregnant = db.Column(db.Boolean, nullable = False, default = False)
  exng = db.Column(db.Boolean, nullable=True)
  heart_disease = db.Column(db.Boolean, nullable=True)
 
  appointments = db.relationship('Appointment', backref ='user', lazy=True)
  supports = db.relationship('Support', backref ='user', lazy=True)
  notifications = db.relationship('Notification', backref ='user', lazy=True)

  def __repr__(self):
     return f'{self.fullname}'
  

  def get_reset_token(self):
    s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
    return s.dumps({'user_id': self.id})

  @staticmethod
  def verify_reset_token(token, age=3600):
    s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
    try:
      user_id = s.loads(token, max_age=age)['user_id']
    except:
      return None
    return User.query.get(user_id)
  

  def to_dict(self):
    return {"id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "birth_year": self.birth_year,
            " gender": self. gender,
            "phone": self.phone,
            "insurance_num": self.insurance_num,
            "height": self.height,
            "weight": self. weight,
            "smoke":self.smoke,
            "num_of_pregnancies": self.num_of_pregnancies,
            "is_pregnant": self.is_pregnant,
            "exng": self.exng,
            "heart_disease": self.heart_disease,
            }
 
  

class Lab(db.Model):
  id = db.Column(db.Integer, primary_key= True)
  name = db.Column(db.String(120), nullable= False)
  location = db.Column(db.Text, nullable= True)

  appointments = db.relationship('Appointment', backref ='lab', lazy=True)

  def __repr__(self):
     return f'{self.name}'
  
  def to_dict(self):
    return {"id": self.id,
            "name": self.name,
            "location": self.location,
            }



class Test(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable= False, unique=True)
  overview = db.Column(db.Text, nullable= False)
  preparation = db.Column(db.Text, nullable= False)
  postparation = db.Column(db.Text, nullable= True)
  duration = db.Column(db.Integer, nullable= False, default = 10) #in minutes

  appointments = db.relationship('Appointment', backref ='test', lazy = True, cascade="all, delete-orphan")
  
  measures = db.relationship('Measure', back_populates='test', lazy=True, cascade="all, delete-orphan")

 
  def __repr__(self):
    return f'{self.name}'
  
  def to_dict(self):
    return {"name": self.name,
            "overview": self.overview,
            "preparation": self.preparation,
            "is_postparation": self.postparation,
            "duration": self.duration,
            # need to test if its working correctly
            "measures": [measure.name for measure in self.measures]
            }  
  

  
class Measure(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable= False)
  name = db.Column(db.Text, nullable=False) 
  test = db.relationship('Test', back_populates='measures', lazy=True)

  results = db.relationship('ResultField', backref= 'measure', lazy= True, cascade="all, delete-orphan")

  def __repr__(self):
     return f'{self.name}'



class Appointment(db.Model):
  id = db.Column(db.Integer, primary_key=True)   
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable= False)
  test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable= False)
  doctor_notes = db.Column(db.String(200), nullable=False, default = "None")
  is_done = db.Column(db.Boolean, nullable= False, default= False)
  # Scheduled, Confirmed, Rescheduled, Canceled, Cancellation Requested, Done 
  state = db.Column(db.String(60), nullable= False, default = "Scheduled") 
 # if server clock different than local clock correct this by add or substract  
 # timedelta(hours = x)
  date = db.Column(db.DateTime, nullable= False)               
  creation_date= db.Column(db.DateTime, nullable= False, default= lambda: datetime.now())

  results = db.relationship('ResultField', backref= 'appointment',
                             cascade='all, delete-orphan' )

  def to_dict(self):
    return {"id": self.id,
            "user_id": self.user_id,
            "lab_id": self.lab_id,
            "test_id": self.test_id,
            "doctor_notes": self.doctor_notes,
            "is_done": self.is_done,
            "state": self.state,
            "time": self.date,
            "creation_time": self.creation_date,
            }


  
class ResultField(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable= False)
  measure_id = db.Column(db.Integer, db.ForeignKey('measure.id'), nullable= False)
  value = db.Column(db.String(180), nullable=False)  
  classification = db.Column(db.String(50), nullable= True)

  __table_args__ = (
        db.UniqueConstraint('appointment_id', 'measure_id', name='unique_appointment_per_measure'),
    )
  
 

class Notification(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  content = db.Column(db.Text, nullable= False, default= '')  
  is_read = db.Column(db.Boolean, nullable= False, default= False)
  creation_date= db.Column(db.DateTime, nullable= False, default= lambda: datetime.now())


  def to_dict(self):
    return {"id": self.id,"content": self.content,
            "is_read": self.is_read, "creation_date": self.creation_date}



class Support(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  title = db.Column( db.String(80), nullable = False )
  description = db.Column(db.Text, nullable = False)



class QA(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(120), nullable=False)
   answer = db.Column(db.String(120), nullable=False)

   def to_dict(self):
    return {"question": self.question,"answer": self.answer}
