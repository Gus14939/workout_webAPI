from marshmallow import fields
from init import db, ma


class SetsReps(db.Model):
    __tablename__ = "sets_and_reps_table"
    
    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise_table.id"), nullable=False)
    
    
    
    user = db.relationship("User", back_populates="sets_reps")
    exercises = db.relationship("Exercise", back_populates="sets_reps")

class SetsRepsSchema(ma.Schema):
    
    user = fields.Nested("UserSchema", only=["name", "email"])
    
    exercises = fields.Nested("ExerciseSchema", only=["name"])
    
    class Meta:
        # fields = ("id", "sets", "reps", "user")
        fields = ("id", "sets", "reps", "user", "exercises")

set_rep_schema = SetsRepsSchema()
sets_reps_schema = SetsRepsSchema(many=True)