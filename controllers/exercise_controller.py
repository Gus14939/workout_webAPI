from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.routine import Routine
from models.exercise import Exercise, exercise_schema, exercises_schema
from models.user import User

from controllers.sets_reps_controller import sets_reps_bp

exercise_bp = Blueprint("exercises", __name__, url_prefix="/<int:routine_id>/exercises")

exercise_only_bp = Blueprint("exercises_only", __name__, url_prefix="/exercises")

exercise_only_bp.register_blueprint(sets_reps_bp)

# The Read - part of CRUD
@exercise_only_bp.route("/")
def get_all_exercises():
    stmt = db.select(Exercise).order_by(Exercise.id)
    exercises = db.session.scalars(stmt)
    return exercises_schema.dump(exercises)

@exercise_only_bp.route("/<exercise_name>")
def get_exercise_byName(exercise_name):
    stmt = db.select(Exercise).filter_by(name=exercise_name)
    one_exercise = db.session.scalar(stmt)
    if one_exercise:
        return exercise_schema.dump(one_exercise)
    else:
        return {"error": f"'{exercise_name}' exercise hasn't been created yet"}, 404

# The Update - part of CRUD
# @exercise_only_bp.route("/<int:exercise_id>", methods=["PATCH", "PUT"])
# @jwt_required()
# def update_exercise(exercise_id):
#     body_data = exercise_schema.load(request.get_json())
    
#     stmt = db.select(Exercise).filter_by(id = exercise_id)
#     exercise = db.session.scalar(stmt)
    
#     if exercise:
#         if str(exercise.user_id) != get_jwt_identity():
#             return {"error": f"Only the creator of the routine can edit this exercise"}, 403
#         exercise.name = body_data.get("name") or exercise.name
#         exercise.category = body_data.get("category") or exercise.category
#         exercise.muscles = body_data.get("muscles") or exercise.muscles
#         exercise.description = body_data.get("description") or exercise.description
    
#         db.session.commit()
#         return exercise_schema.dump(exercise)
#     else:
#         return {"message": f"Exercise not found"}, 404
     
# # The Delete - part of CRUD
# @exercise_only_bp.route("/<int:exercise_id>", methods=["DELETE"])
# @jwt_required()
# def delete_exercise(exercise_id):
#     stmt = db.select(Exercise).filter_by(id=exercise_id)
#     exercise = db.session.scalar(stmt)
     
#     db.session.delete(exercise)
#     db.session.commit()

# CREATE Exercises views from Routines 

@exercise_bp.route('/', methods=["POST"])
@jwt_required()
def create_exrcise_in_routine(routine_id):
    body_data = exercise_schema.load(request.get_json())
    
    stmt = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(stmt)
    
    if routine:
        if str(routine.user_id) != get_jwt_identity():
            return {"error": f"Only the creator of '{routine.name}' routine can add exercises to it"}, 403
        exercise = Exercise(
            name = body_data.get("name"),
            category = body_data.get("category"),
            muscles = body_data.get("muscles"),
            description = body_data.get("description"),
            user_id = get_jwt_identity(),
            routine_id = routine_id
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise_schema.dump(exercise), 201
    else:
        return {"error": f"Routine with id {routine_id} doesn't exist"}, 404
    
@exercise_bp.route('/<int:exercise_id>', methods=["DELETE"])
@jwt_required()
def delete_exrcise_in_routine(routine_id, exercise_id):
    stmt = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt)
    
    routine_stmt = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(routine_stmt)
     
    if exercise and exercise.routine_id == routine_id:
        if str(exercise.user_id) != get_jwt_identity():
            return {"error": "Only the creator can delete this exercise"}, 403
        db.session.delete(exercise)
        db.session.commit()
        return {"message": f"{exercise.name} exercise has been removed from {routine.weekday} routine"}
    else:
        return {"error": f"This exercise does not exist in your {routine.weekday} routine"}, 404
        
@exercise_bp.route('/<int:exercise_id>', methods=["PUT", "PATCH"])
@jwt_required()
def edit_exrcise_in_routine(routine_id, exercise_id):
    body_data = exercise_schema.load(request.get_json())
    stmt = db.select(Exercise).filter_by(id=exercise_id, routine_id=routine_id)
    exercise = db.session.scalar(stmt)
    
    stmt_routine = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(stmt_routine)
    
    if exercise:
        if str(exercise.user_id) != get_jwt_identity():
            return {"error": "Only the creator can can edit this exercise"}, 403
        exercise.name = body_data.get("name") or exercise.name
        exercise.category = body_data.get("category") or exercise.category
        exercise.muscles = body_data.get("muscles") or exercise.muscles
        exercise.description = body_data.get("description") or exercise.description
    
        db.session.commit()
        return exercise_schema.dump(exercise)
    else:
        return {"error": f"Exercise not found in '{routine.weekday}' routine"}, 404


def is_user_admin():
    user_id = get_jwt_identity
    stmt =  db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin