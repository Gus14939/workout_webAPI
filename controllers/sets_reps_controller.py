from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.exercise import Exercise
from models.sets_reps import SetsReps, set_rep_schema

sets_reps_bp = Blueprint("set_and_reps", __name__, url_prefix="/<int:exercise_id>/sets_and_reps")

@sets_reps_bp.route("/", methods=["POST"])
@jwt_required()
def create_sets_reps(exercise_id):
    body_data = set_rep_schema.load(request.get_json(), partial=True)
    stmt = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt)
    
    stmt_set_rep = db.select(SetsReps).filter_by(exercise_id=exercise_id)
    set_rep = db.session.scalar(stmt_set_rep)
    
    if exercise.sets_reps:
        return [{"error": f"There are asigned sets and reps to '{exercise.name}'"},{"Sets and Reps Assigned": f"set: {set_rep.sets}, repetitons: {set_rep.reps}, goal: {set_rep.goal}"}], 409
    
    if exercise:
        if str(exercise.user_id) != get_jwt_identity():
            return {"error": f"Only the creator of '{exercise.name}' can add sets and reps"}, 403
        set_rep = SetsReps(
            sets = body_data.get("sets"),
            reps = body_data.get("reps"),
            goal = body_data.get("goal"),
            exercise_id = exercise_id,           
            user_id = get_jwt_identity()
        )
        db.session.add(set_rep)
        db.session.commit()
        return set_rep_schema.dump(set_rep), 201
    else:
        return {"error": f"'exercise' not found"}, 404

@sets_reps_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_sets_reps(exercise_id):
    stmt = db.select(SetsReps).filter_by(exercise_id=exercise_id)
    set_rep = db.session.scalar(stmt)
    
    stmt_exercise = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt_exercise)
    
    if exercise:
        if str(exercise.user_id) != get_jwt_identity():
            return {"error": f"Only the creator of '{exercise.name}' can delete its associted sets and reps"}, 403
        db.session.delete(set_rep)
        db.session.commit()
        return {"message": f"sets and reps for '{exercise.name}' have been deleted"}
    else:
        return {"error": f"Not found, sets or reps are not yet set up for this exercise"}, 404
    
@sets_reps_bp.route("/<int:sets_reps_id>", methods=["PATCH", "PUT"])
@jwt_required()
def edit_sets_reps(exercise_id, sets_reps_id):
    body_data = set_rep_schema.load(request.get_json(), partial=True)
    stmt = db.select(SetsReps).filter_by(id=sets_reps_id, exercise_id=exercise_id)
    set_rep = db.session.scalar(stmt)
    
    stmt_exercise = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt_exercise)
    
    if set_rep:
        if str(set_rep.user_id) != get_jwt_identity():
            return {"error": f"These sets and reps are associted to another user's exercise, you cannot modify it"}, 403
        set_rep.sets = body_data.get("sets") or set_rep.sets
        set_rep.reps = body_data.get("reps") or set_rep.reps
        set_rep.goal = body_data.get("goal") or set_rep.goal
        
        db.session.commit()
        return set_rep_schema.dump(set_rep)
    elif not exercise:
        return {"error": f"Exercise not found"}, 404
    else:
        return {"error": f"No sets and reps found with id {sets_reps_id}"}, 404