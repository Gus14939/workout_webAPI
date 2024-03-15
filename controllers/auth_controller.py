from datetime import date, timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema

# my tries
from email_validator import validate_email, EmailNotValidError


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # from body data
        body_data = request.get_json()
        print("Received data:", body_data)  # print line for debugging
        
        # validate email
        email = body_data.get("email")
        try:
            valid_email_syntax = validate_email(email)
            normalised_email = valid_email_syntax.email            
        except EmailNotValidError as e:
            return {"error": str(e)}, 400
        
        name = body_data.get("name")
        age = body_data.get("age")
        weight = body_data.get("weight")
        height = body_data.get("height")
        gender = body_data.get("gender")

            
        # create user instance
        new_user = User(
            name = name,
            email = normalised_email,
            age = age,
            weight = weight,
            height = height,
            gender = gender,
            date_joined = date.today()
            # is_admin
        )
        
        # password from body data
        password = body_data.get("password")
        if password:
            new_user.password = bcrypt.generate_password_hash(password).decode('utf-8')    
             
        # add and commit to DB
        db.session.add(new_user)
        db.session.commit()
        
        # return to respond the client
        return user_schema.dump(new_user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email is already in use"}, 409
         # Handle other exceptions as necessary
        return {"error": "An error occurred"}, 500
    except ValueError as e:
        return {"error": str(e)}, 400
    
    


@auth_bp.route("/login", methods=["POST"])
def auth_login():
    
    # get the data from the request body
    body_data = request.get_json()
    # Find the user with the email address
    stmt = db.select(User).filter_by(email = body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create jwt
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=15))
        # return the token along with the user info
        return {"name": user.name, "email": user.email, "token": token, "is_admin": user.is_admin, "user":user.id}
    # else
    else:
        # return error
        return {"error": "Incorrect Credentials - Check your email or password"}, 401