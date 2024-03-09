# from datetime import datetime

from flask import Blueprint, request
# from sqlalchemy.exc import IntegrityError
# from flask_jwt_extended import create_access_token
# from psycopg2 import errorcodes

from init import db, bcrypt
from models.routine import Routine, routines_schema

routines_bp = Blueprint("routines", __name__, url_prefix="/routines")

@routines_bp.route("/")
def get_all_routines():
    stmt = db.select(Routine).order_by(Routine.weekday)
    routines = db.session.scalars(stmt)
    return routines_schema.dump(routines)