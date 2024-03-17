# from flask import Blueprint
# from flask_jwt_extended import jwt_required, get_jwt_identity

# from init import db, ma
# from models.user import User, user_schema, users_schema



# user_bp = Blueprint("profile", __name__, url_prefix="/profile")


# # Read
# @user_bp.route("/")
# def get_users():
#     stmt = db.select(User).order_by(User.id)
#     # stmt = db.select(User).filter_by(User.id)
#     profile = db.session.scalars(stmt)
#     return users_schema.dump(profile)