from marshmallow import fields
from init import db, ma

class User(db.Model):
    __tablename__ = "user_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    weight = db.Column(db.String, nullable=False)
    height = db.Column(db.String, nullable=False)  
    gender = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date) 
    is_admin = db.Column(db.Boolean, default=False)
    
    routines = db.relationship("Routine", back_populates="user", cascade="all, delete")
    
    exercises = db.relationship("Exercise", back_populates="user", cascade="all, delete")
    
    
class UserSchema(ma.Schema):
    
    routines = fields.List(fields.Nested("RoutineSchema", exclude=["user"]))
    
    exercises = fields.List(fields.Nested("ExerciseSchema", exclude=["user"]))
    
    class Meta:
        fields = ("id", "name", "email", "password", "age", "weight", "height", "gender", "date_joined", "is_admin", "routines", "exercises")
        

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
        
        