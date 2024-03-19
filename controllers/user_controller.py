from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.user import User, user_schema, users_schema


profile_bp = Blueprint("user_profile", __name__, url_prefix="/profile")

@profile_bp.route("/", methods=["GET"])
def get_profiles():
    stmt = db.select(User).order_by(User.id)
    profiles = db.session.scalars(stmt)
    
    return users_schema.dump(profiles)

@profile_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_one_profile(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    if profile:
        return user_schema.dump(profile)
    else:
       return {"error": f"User {user_id} does not exist"}, 404
    

@profile_bp.route("/<int:user_id>", methods=["PATCH", "PUT"])
def edit_profile(user_id):
    
    body_data = request.get_json()
    
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    if profile:
        profile.weight = body_data.get("weight") or profile.weight
        db.session.commit()
        return {"message": f"{profile.name}'s weight is now {profile.weight}kg"}
    else:
       return {"error": f"{profile.id} does not exist"}, 404
            

@profile_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_profile(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    if profile:
       db.session.delete(profile) 
       db.session.commit()
       return {"message": f"{profile.name} profile has now been deleted"}
    else:
       return {"error": f"{profile.name} does not exist"}, 404