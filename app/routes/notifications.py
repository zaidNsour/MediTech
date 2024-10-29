from flask import Blueprint, jsonify, request
from app.models import  Notification, User
from app.utils import admin_required
from app.validators import validate_content
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app import db


bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.route("/add_notification", methods=[ "POST"])
@admin_required
def add_notification():
  try:
    data = request.get_json()
    user_id = data.get("user_id")   
    content = data.get("content")      
    
      
    if not all([user_id,content]):
      return jsonify({'message': 'missing user_id or content'}), 400 
    
    user = User.query.get(user_id)

    if not user:
      return jsonify({'message': 'User not found.'}), 400     
    
    if not validate_content(content):
      return jsonify({'message': 'Invalid content.'}), 400
    

    notification = Notification(user_id= user_id, content= content)    
          
    db.session.add( notification)
    db.session.commit()
    return jsonify({'message': 'Notification created successfully!'}), 200
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': f'Database error occurred while create Notification.'}), 500
    
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while create Notification.'}), 500
  

@bp.route('/notifications', methods=['GET'])
@login_required
def notifications():
  try:
    user_id = current_user.id

    notifications = Notification.query.filter_by(user_id= user_id).all()
    return jsonify([n.to_dict() for n in notifications])  
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while fetch the notifications.'}), 500
  


@bp.route('/mark_as_read', methods= ['PATCH'])
def mark_as_read():
  try:
    data = request.get_json()
    notification_id = data.get("notification_id")
    if not notification_id:
      return jsonify({'message': 'missing notification_id.'}), 400  

    notificaiton = Notification.query.get(notification_id)

    if not notificaiton:
      return jsonify({'message': 'invalid notification_id.'}), 400  
    
    notificaiton.is_read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked as read successfully!'}), 200
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'message': f'Database error occurred while mark the notification as read.'}), 500
  
  except Exception as e:
    return jsonify({'message': 'An unexpected error occurred while mark the notification as read.'}), 500
