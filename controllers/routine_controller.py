from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.routine import Routine, routines_schema, routine_schema, WEEKDAYS

from controllers.exercise_controller import exercise_bp


routine_bp = Blueprint("routines", __name__, url_prefix="/routines")
routine_bp.register_blueprint(exercise_bp) 

# The Read - part of CRUD - it does not required authentication
# "/routines"
# HTTP GET request. This view retrieves all routines in the database
@routine_bp.route("/")
def get_all_routines():
    stmt = db.select(Routine).order_by(Routine.id)
    routines = db.session.scalars(stmt)
    return routines_schema.dump(routines)

# "/routines/<routine_id>"
# HTTP GET request. This view retrieves one routine filtered by the id
# Returns 200, 404
@routine_bp.route("/<int:routine_id>")
def get_routine_byID(routine_id):
    stmt = db.select(Routine).filter_by(id=routine_id)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine with 'id {routine_id}' hasn't been setup yet"}, 404

# "/routines/<routine_name>"
# HTTP GET request. This view retrieves one routine filtered by the name
# Returns 200, 404
@routine_bp.route("/name/<routine_name>")
def get_routine_byName(routine_name):
    stmt = db.select(Routine).filter_by(name=routine_name)
    one_routine = db.session.scalar(stmt)
    if one_routine:
        return routine_schema.dump(one_routine)
    else:
        return {"error": f"Routine for '{routine_name}' hasn't been setup yet"}, 404

# "/routines/<routine_weekday>"
# HTTP GET request. This view retrieves one routine filtered by the day of the week
# Returns 200, 404
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
# "/routines/<routine_id>"
# HTTP POST request. A registered user can create a routine
# Requires authentication
@routine_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_routine():
    body_data = routine_schema.load(request.get_json())
    stmt = db.select(Routine)
    routine = db.session.scalar(stmt)
    
    # Create a new routine model instance
    routine = Routine(
        name = body_data.get("name"),
        description = body_data.get("description"),
        weekday = body_data.get("weekday"),
        user_id = get_jwt_identity()
    )
    
    # add to the session and commit
    db.session.add(routine)
    db.session.commit()
    # return the newly cerated routine
    return routine_schema.dump(routine), 201
        
# The Update - part of CRUD
# "/routines/<routine_id>"
# HTTP PATCH request. A registered user can modify a routine
# Requires authentication
# Returns 200, 403, 404
@routine_bp.route("/<int:routine_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_routine(routine_id):
    body_data = routine_schema.load(request.get_json(), partial=True)
    
    stmt = db.select(Routine).filter_by(id = routine_id)
    routine = db.session.scalar(stmt)
    
    if routine:
        if str(routine.user_id) != get_jwt_identity():
            print(routine.user)
            return {"error": "Only the creator of the routine can edit it"}, 403
    
        routine.name = body_data.get("name") or routine.name
        routine.description = body_data.get("description") or routine.description
        routine.weekday = body_data.get("weekday") or routine.weekday
        
        db.session.commit()
        return routine_schema.dump(routine)
    else:
        return {"message": f"Routine not found"}, 404
        
# The Delete - part of CRUD
# "/routines/<routine_id>"
# HTTP DELETE request. A registered user can remove a routine
# Requires authentication
# Returns 200, 403 , 404
@routine_bp.route("/<int:routine_id>", methods=["DELETE"])
@jwt_required()
def delete_routine(routine_id):
    stmt = db.select(Routine).where(Routine.id == routine_id)
    routine = db.session.scalar(stmt)
    if routine:
        if str(routine.user_id) != get_jwt_identity():
            return {"error": "Only the creator can delete this routine"}, 403
        db.session.delete(routine)
        db.session.commit() 
        return {"message": f"{routine.name} routine for {routine.weekday} has now been deleted"}
    else:
        return {"message": f"Routine not found"}, 404
    