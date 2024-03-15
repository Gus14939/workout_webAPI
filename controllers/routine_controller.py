from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.routine import Routine, routines_schema, routine_schema
# from controllers.exercise_controller import exercise_bp
from models.exercise import Exercise, exercise_schema

routine_bp = Blueprint("routines", __name__, url_prefix="/routines")
# routine_bp.register_blueprint(exercise_bp) 

# The Read - part of CRUD
@routine_bp.route("/")
def get_all_routines():
    stmt = db.select(Routine).order_by(Routine.id)
    routines = db.session.scalars(stmt)
    return routines_schema.dump(routines)

@routine_bp.route("/<int:routine_id>")
def get_routine_byID(routine_id):
    stmt = db.select(Routine).filter_by(id=routine_id)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine with '{routine_id}' hasn't been setup yet"}, 404
    
@routine_bp.route("/name/<routine_name>")
def get_routine_byName(routine_name):
    stmt = db.select(Routine).filter_by(name=routine_name)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine for '{routine_name}' hasn't been setup yet"}, 404

@routine_bp.route("/day/<routine_Day>")
def get_routine_byDay(routine_Day):
    stmt = db.select(Routine).filter_by(weekday=routine_Day)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        print(one_routine)
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine for '{routine_Day}' hasn't been setup yet"}, 404

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
@routine_bp.route("/<int:routine_id>", methods=["PATCH", "PUT"])
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
@routine_bp.route("/<int:routine_id>", methods=["DELETE"])
@jwt_required()
def delete_routine(routine_id):
    stmt = db.select(Routine).where(Routine.id == routine_id)
    routine = db.session.scalar(stmt)
    if routine:
        db.session.delete(routine)
        db.session.commit() 
        return {"message": f"{routine.name} routine for {routine.weekday} has now been deleted"}
    else:
        return {"message": f"Routine not found"}, 404
    
    
# ("/routines/<int:routine_id>/exercises") --> GET, POST
# ("/routines/1/exercises") --> GET, POST

# ("/routines/<int:routine_id>/<int:exercises>") --> PUT, PATCH, DELETE
# ("/routines/1/exercises/2") --> PUT, PATCH, DELETE

# CREATE Exercises into Routines 
@routine_bp.route('<int:routine_id>/exercises', methods=["POST"])
@jwt_required()
def create_comment(routine_id):
    body_data = request.get_json()
    stmt = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(stmt)
    if routine:
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
    
@routine_bp.route('<int:routine_id>/exercises/<int:exercise_id>', methods=["DELETE"])
@jwt_required()
def delete_comment(routine_id, exercise_id):
    stmt = db.select(Exercise).filter_by(id=exercise_id)#, routine=routine_id)
    exercise = db.session.scalar(stmt)
    
    routine_stmt = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(routine_stmt)
     
    if exercise and exercise.routine_id == routine_id:
        db.session.delete(exercise)
        db.session.commit()
        return {"message": f"{exercise.name} exercise has been removed from {routine.weekday} routine"}
    else:
        return {"error": f"This exercise does not exist in your {routine.weekday} routine"}, 404
        # return {"error": f"Routine {routine_id} or exercise doesn't exist"}
        
@routine_bp.route('<int:routine_id>/exercises/<int:exercise_id>', methods=["PUT", "PATCH"])
@jwt_required()
def edit_comment(routine_id, exercise_id):
    body_data = request.get_json()
    stmt = db.select(Exercise).filter_by(id=exercise_id, routine_id=routine_id)
    exercise = db.session.scalar(stmt)
    
    stmt_routine = db.select(Routine).filter_by(id=routine_id)
    routine = db.session.scalar(stmt_routine)
    
    if exercise:
        exercise.name = body_data.get("name") or exercise.name
        exercise.category = body_data.get("category") or exercise.category
        exercise.muscles = body_data.get("muscles") or exercise.muscles
        exercise.description = body_data.get("description") or exercise.description
    
        db.session.commit()
        return exercise_schema.dump(exercise)
    else:
        return {"error": f"Exercise not found in {routine.weekday} routine"}, 404
    