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