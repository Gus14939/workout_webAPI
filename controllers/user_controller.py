from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.user import User, user_schema, users_schema

profile_bp = Blueprint("user_profile", __name__, url_prefix="/profile")

# The Read - part of CRUD
# "/profile"
# HTTP GET request. Retrieves all users in the database
@profile_bp.route("/")
def get_profiles():
    stmt = db.select(User).order_by(User.id)
    profiles = db.session.scalars(stmt)
    
    return users_schema.dump(profiles)

# "/profile/<user_id>"
# HTTP GET request. Retrieves a specific user or profile
@profile_bp.route("/<int:user_id>")
@jwt_required()
def get_one_profile(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    if profile:
        return user_schema.dump(profile)
    else:
       return {"error": f"User {user_id} does not exist"}, 404
    
# The Update - part of CRUD
# "/profile/<user_id>"
# HTTP PATCH, PUT request. This view allows the user to update the profile
# Requires the user to be the owner of the profile - requires authentication
@profile_bp.route("/<int:user_id>", methods=["PATCH", "PUT"])
@jwt_required()
def edit_profile(user_id):
    
    body_data = user_schema.load(request.get_json(), partial=True)
    
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    
    if profile:
        if str(profile.id) != get_jwt_identity():
            return {"error": "Only the profile owner can edit this routine"}, 403
        
        profile.weight = body_data.get("weight") or profile.weight
        db.session.commit()
        return {"message": f"{profile.name}'s weight is now {profile.weight}kg"}
    else:
       return {"error": f"{profile.id} does not exist"}, 404

# The Delete - part of CRUD
# "/profile/<user_id>"
# HTTP DELETE request. This view allows the user and/or the admin to delete the profile
# Requires authentication
@profile_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_profile(user_id):
    
    is_admin = is_user_admin()
    
    stmt = db.select(User).filter_by(id=user_id)
    profile = db.session.scalar(stmt)
    print(is_admin)
    if profile:
        if not is_admin:
            if str(profile.id) != get_jwt_identity():
                return {"error": "Only the profile owner or admin can delete this routine"}, 403
            # return {"error": "Not authorised to delete a card"}, 403
        
        db.session.delete(profile) 
        db.session.commit()
        return {"message": f"{profile.name} profile has now been deleted"}
    else:
        return {"error": f"{profile.name} does not exist"}, 404
   
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin