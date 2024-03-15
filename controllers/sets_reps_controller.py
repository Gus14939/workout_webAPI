from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.sets_reps import SetsReps, set_rep_schema, sets_reps_schema

sets_reps_bp = Blueprint("set_and_reps", __name__, url_prefix="/sets_and_reps")

# The Read - part of CRUD
'''
@sets_reps_bp.route("/")s
def get_all_sets_reps():
    stmt = db.select(SetsReps).order_by(SetsReps.id)
    sets_and_reps = db.session.scalars(stmt)
    return sets_reps_schema.dump(sets_and_reps)

@sets_reps_bp.route("/<set_and_rep_id>")
def get_set_and_rep_byID(set_and_rep_id):
    stmt = db.select(SetsReps).filter_by(name=set_and_rep_id)
    set_and_rep = db.session.scalar(stmt)
    if set_and_rep:
        return set_rep_schema.dump(set_and_rep)
    else:
        return {"error": f"'{set_and_rep_id}' exercise hasn't been created yet"}, 404


# The Create - part of CRUD
@exercise_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_exercise():
    body_data = request.get_json()
    # body_data = exercise_schema.load(request.get_json())
    # Create a new card model instance
    exercise = Exercise(
        name = body_data.get("name"), # it's unique have to handle errors
        category = body_data.get("category"),
        muscles = body_data.get("muscles"),
        description = body_data.get("description"),
        user_id = get_jwt_identity()
    )
    # add to the session and commit
    db.session.add(exercise)
    db.session.commit()
    # return the newly cerated card
    return exercise_schema.dump(exercise), 201

# The Update - part of CRUD
@exercise_bp.route("/<exercise_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_exercise(exercise_id):
    body_data = request.get_json()
    
    stmt = db.select(Exercise).filter_by(id = exercise_id)
    exercise = db.session.scalar(stmt)
    
    if exercise:
        exercise.name = body_data.get("name") or exercise.name
        exercise.category = body_data.get("category") or exercise.category
        exercise.muscles = body_data.get("muscles") or exercise.muscles
        exercise.description = body_data.get("description") or exercise.description
    
        db.session.commit()
        return exercise_schema.dump(exercise)
    else:
        return {"message": f"Exercise not found"}, 404
     
# The Delete - part of CRUD
@exercise_bp.route("/<exercise_id>", methods=["DELETE"])
@jwt_required()
def delete_exercise(exercise_id):
    stmt = db.select(Exercise).where(Exercise.id == exercise_id)
    exercise = db.session.scalar(stmt)
    if exercise:
        db.session.delete(exercise)
        db.session.commit() 
        return {"message": f"{exercise.name} exercise has now been deleted"}
    else:
        return {"message": f"Exercise not found"}, 404
    '''