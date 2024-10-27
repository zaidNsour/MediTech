
from models import Appointment
from utils import parse_user_info


appointment = Appointment.query.filter_by(id=1).first()

test_name = appointment.test.name
user_info= parse_user_info(appointment.user)
results = appointment.results
doctor_notes = appointment.doctor_notes

print(f'test_name: {test_name}')
print(f'user_info: {user_info}')
print(f'results: {results}')
print(f'doctor_notes: {doctor_notes}')