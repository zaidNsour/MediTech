
from app.models import Lab, User
from app.data import LABS, USERS

def init_db(db):
    print("Initializing database")

     
    if not User.query.first():  

        for user_info in USERS:
            user = User(fullname=user_info['fullname'], email = user_info['email']
                        ,password = user_info['password'], birth_year = user_info['birth_year'],
                        gender = user_info['gender'],height = user_info['height'], 
                        weight = user_info['weight'], smoke = user_info['smoke']
                         )
            
            db.session.add(user)

    if not Lab.query.first():  # Check if locations exist
        for lab_info in LABS:
            lab = Lab(name= lab_info['name'], location= lab_info['location'])
            db.session.add(lab)

    db.session.commit()
    



