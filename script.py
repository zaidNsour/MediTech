from app import create_app


app = create_app()

from app.utils import classify_result_value

with app.app_context():
  print(classify_result_value("glucose level mg/dL","male",160))


