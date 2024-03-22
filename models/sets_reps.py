from marshmallow import fields, validate
from marshmallow.validate import OneOf

from init import db, ma

GOALS = ("Tone", "Definition", "Endurance", "Power", "Strength")

class SetsReps(db.Model):
    __tablename__ = "sets_and_reps_table"
    
    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    goal = db.Column(db.String(20))
    
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise_table.id"), nullable=False)
    
    
    
    user = db.relationship("User", back_populates="sets_reps")
    exercises = db.relationship("Exercise", back_populates="sets_reps")

class SetsRepsSchema(ma.Schema):
    
    # Validation
    sets = fields.Integer(strict=True, required=True, validate=[validate.Range(min=1, max=99, error="Value must be greater than 0 and no bigger than 99")])
    
    reps = fields.Integer(strict=True, required=True, validate=[validate.Range(min=1, max=99, error="Value must be greater than 0 and no bigger than 99")])
    
    goal = fields.String(validate=OneOf(GOALS))
    
    user = fields.Nested("UserSchema", only=["name", "email"])
    
    exercises = fields.Nested("ExerciseSchema", only=["name"])
    
    class Meta:
        # fields = ("id", "sets", "reps", "user")
        fields = ("id", "sets", "reps", "goal", "exercises", "user")

set_rep_schema = SetsRepsSchema()
sets_reps_schema = SetsRepsSchema(many=True)