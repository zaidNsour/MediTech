from functools import wraps
from flask import jsonify
import datetime
from flask_login import current_user, login_required

current_year = datetime.datetime.now().year


def admin_required(fn):
  @wraps(fn)
  @login_required
  def wrapper(*args, **kwargs):
    user = current_user
    if not user or not user.is_admin:
      return jsonify({"message": "Admin access required"}), 403
    return fn(*args, **kwargs)
  return wrapper





  

   