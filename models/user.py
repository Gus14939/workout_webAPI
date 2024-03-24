from marshmallow import fields, validate
from marshmallow.validate import Length, And, Regexp, OneOf

from init import db, ma

GENDER = ("M", "F")

class User(db.Model):
    __tablename__ = "user_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)  
    gender = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date) 
    is_admin = db.Column(db.Boolean, default=False)
    
    routines = db.relationship("Routine", back_populates="user", cascade="all, delete")
    
    exercises = db.relationship("Exercise", back_populates="user", cascade="all, delete")
    
    sets_reps = db.relationship("SetsReps", back_populates="user", cascade="all, delete")
    
class UserSchema(ma.Schema):
    
    # Validation
    name = fields.String(validate=And(
        Length(min=2, max=32, error="The name should be 2 to 32 characters"),
        Regexp('^[A-Za-z -]+$', error="Only Alphabetic characters, dashes")
    ))
    
    # email validation is done in auth_controller.py
    
    password = fields.String(validate=Regexp(
        r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{6,}$',
        error="Password must be at least 6 characters long; contain one or many digits, special characters, lowercase and uppercase letters. No space allowed."
    ))
    
    age = fields.Integer(strict=True, required=True, validate=[validate.Range(min=15, max=99, error="Age must be between 15 an 99 year old")])
    
    weight = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0, max=250, error="Weight must be between 1 an 250kg")])
    
    height = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0, max=250, error="Height must be not greater than 250cm")])
    
    gender = fields.String(validate=OneOf(GENDER))
    
    routines = fields.List(fields.Nested("RoutineSchema", only=["name"]))
    
    exercises = fields.List(fields.Nested("ExerciseSchema", only=["name"]))
    
    sets_reps = fields.List(fields.Nested("SetsReps", exclude=["user"]))
    
    class Meta:
        
        fields = ("id", "name", "email", "password", "age", "weight", "height", "gender", "date_joined", "is_admin", "routines", "exercises", "sets_reps")
        
user_schema = UserSchema(exclude=["routines", "exercises", "sets_reps"])
users_schema = UserSchema(many=True, exclude=["routines", "exercises", "sets_reps"])