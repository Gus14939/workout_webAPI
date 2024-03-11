from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.exercise import Exercise, exercises_schema, exercise_schema

exercise_bp = Blueprint("exercises", __name__, url_prefix="/exercises")

# The Read - part of CRUD
@exercise_bp.route("/")
def get_all_exercises():
    stmt = db.select(Exercise).order_by(Exercise.id)
    exercises = db.session.scalars(stmt)
    return exercises_schema.dump(exercises)

@exercise_bp.route("/name/<exercise_name>")
def get_exercise_byName(exercise_name):
    stmt = db.select(Exercise).filter_by(name=exercise_name)
    one_exercise = db.session.scalar(stmt)
    if one_exercise:
        return exercise_schema.dump(one_exercise)
    else:
        return {"error": f"'{exercise_name}' exercise hasn't been created yet"}, 404

"""
# The Create - part of CRUD
@routine_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_routine():
    body_data = request.get_json()
    # body_data = routine_schema.load(request.get_json())
    # Create a new card model instance
    routine = Routine(
        name = body_data.get("name"), # it's unique have to handle errors
        description = body_data.get("description"),
        weekday = body_data.get("weekday"),
        user_id = get_jwt_identity()
    )
    # add to the session and commit
    db.session.add(routine)
    db.session.commit()
    # return the newly cerated card
    return routine_schema.dump(routine), 201
        
# The Update - part of CRUD
@routine_bp.route("/<routine_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_routine(routine_id):
    body_data = request.get_json()
    
    stmt = db.select(Routine).filter_by(id = routine_id)
    routine = db.session.scalar(stmt)
    
    if routine:
        routine.name = body_data.get("name") or routine.name
        routine.description = body_data.get("description") or routine.description
        routine.weekday = body_data.get("weekday") or routine.weekday
        
        db.session.commit()
        return routine_schema.dump(routine)
    else:
        return {"message": f"Routine not found"}, 404
        
# The Delete - part of CRUD
@routine_bp.route("/<routine_id>", methods=["DELETE"])
@jwt_required()
def delete_routine(routine_id):
    stmt = db.select(Routine).where(Routine.id == routine_id)
    routine = db.session.scalar(stmt)
    if routine:
        db.session.delete(routine)
        db.session.commit() 
        return {"message": f"Routine of {routine.name} for {routine.weekday} has now been deleted"}
    else:
        return {"message": f"Routine not found"}, 404
    
    """