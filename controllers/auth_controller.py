from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # from body data
        body_data = request.get_json()
        # password from body data
        password = body_data.get("password")

        # create user instance
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email"),
            
            date_joined = body_data.get("date_joined"),
            age = body_data.get("age"),
            weight = body_data.get("weight"),
            height = body_data.get("height"),
            gender = body_data.get("gender")
            # is_admin
        )
        
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
             
        # add and commit to DB
        db.session.add(user)
        db.session.commit()
        
        # return to respond the client
        return user_schema.dump(user), 201

    except IntegrityError:
        return {"error": "Email is already in use"}, 409
    