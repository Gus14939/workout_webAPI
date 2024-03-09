from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema



routines_bp = Blueprint("routines", __name__, url_prefix="/routines")

@routines_bp.route("/", methods=["POST"])
def get_routines():
    pass