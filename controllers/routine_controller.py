from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db, bcrypt
from models.routine import Routine, routines_schema, routine_schema

routines_bp = Blueprint("routines", __name__, url_prefix="/routines")

# The Read - part of CRUD
@routines_bp.route("/")
def get_all_routines():
    stmt = db.select(Routine).order_by(Routine.id)
    routines = db.session.scalars(stmt)
    return routines_schema.dump(routines)

@routines_bp.route("name/<routine_name>")
def get_routine_byName(routine_name):
    stmt = db.select(Routine).filter_by(name=routine_name)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine for '{routine_name}' hasn't been setup yet"}, 404

@routines_bp.route("/day/<routine_Day>")
def get_routine_byDay(routine_Day):
    stmt = db.select(Routine).filter_by(weekday=routine_Day)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        print(one_routine)
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine for '{routine_Day}' hasn't been setup yet"}, 404

# The Create - part of CRUD
@routines_bp.route("/", methods=["POST"])
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
@routines_bp.route("/<routine_id>", methods=["PATCH", "PUT"])
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
@routines_bp.route("/<routine_id>", methods=["DELETE"])
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