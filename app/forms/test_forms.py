from flask_wtf import FlaskForm
from wtforms import DecimalField, FloatField, IntegerField, BooleanField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class HeartFailureForm(FlaskForm):
  creatinine_phosphokinase = FloatField('Creatinine Phosphokinase (mcg/L):', validators=[DataRequired()])
  ejection_fraction = FloatField('Ejection Fraction (%):', validators=[DataRequired()])
  platelets = FloatField('Platelets (kiloplatelets/mL):', validators=[DataRequired()])
  serum_creatinine = FloatField('Serum Creatinine (mg/dL):', validators=[DataRequired()])
  serum_sodium = FloatField('Serum Sodium (mEq/L):', validators=[DataRequired()])
  anaemia = BooleanField('Anaemia')
  diabetes = BooleanField('Diabetes')
  high_blood_pressure = BooleanField('High Blood Pressure')

  submit = SubmitField('Save')


class DiabetsForm(FlaskForm):
  glucose = FloatField('Plasma glucose concentration:', validators=[DataRequired()])
  blood_pressure = FloatField('Diastolic blood pressure (mm Hg):', validators=[DataRequired()])
  skin_thickness = FloatField('Triceps skin fold thickness (mm):', validators=[DataRequired()])
  insulin = FloatField('2-Hour serum insulin (mu U/ml):', validators=[DataRequired()])
  pedigree= FloatField('Diabetes pedigree function:', validators=[DataRequired()])
  
  submit = SubmitField('Save')


class HeartAttackForm(FlaskForm):
    chest_pain = SelectField('Chest Pain Type:', 
                              choices=[('TA', 'Typical Angina'),
                                       ('ATA', 'Atypical Angina'),
                                       ('NAP', 'Non-Anginal Pain'),
                                       ('ASY', 'Asymptomatic')],
                              validators=[DataRequired()])
    
    blood_pressure = FloatField('Blood Pressure (mm Hg):', 
                                 validators=[DataRequired()])
    
    cholesterol = FloatField('Cholesterol (mg/dl):', 
                             validators=[DataRequired()])
    
    fasting_blood_sugar = FloatField('Fasting Blood Sugar (mg/dl):', 
                                      validators=[DataRequired()])
    
    resting_ECG = SelectField('Resting ECG:', 
                              choices=[('Normal', 'Normal'),
                                       ('ST', 'ST-T Wave Abnormality'),
                                       ('LVH', 'Left Ventricular Hypertrophy')],
                              validators=[DataRequired()])
    
    max_heart_rate = FloatField('Max Heart Rate:', 
                                 validators=[DataRequired()])
    
    oldpeak = FloatField('ST Depression:', 
                         validators=[DataRequired()])
    
    slope = SelectField('Slope of the Peak Exercise ST Segment:', 
                        choices=[('Up', 'Upsloping'),
                                 ('Flat', 'Flat'),
                                 ('Down', 'Downsloping')],
                        validators=[DataRequired()])
    
    major_vessels = SelectField('Number of Major Vessels:', 
                                 choices=[('0', '0'),
                                          ('1', '1'),
                                          ('2', '2'),
                                          ('3', '3')],
                                 validators=[DataRequired()])
    
    thal_rate = SelectField('Thal Rate:', 
                             choices=[('normal', 'Normal'),
                                      ('fixed_defect', 'Fixed Defect'),
                                      ('reversible_defect', 'Reversible Defect')],
                             validators=[DataRequired()])
    
    submit = SubmitField('Save')


class StrokeForm(FlaskForm):
  glucose = FloatField('Average glucose level in blood:', validators=[DataRequired()])
  hypertension = BooleanField('Hypertension')  # Checkbox field
  submit = SubmitField('Save')

       
    