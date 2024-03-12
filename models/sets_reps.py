from marshmallow import fields
from init import db, ma


class SetsReps(db.Model):
    __tablename__ = "sets_and_reps_table"
    
    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    
    # exercise_id = db.Column(db.Integer, db.ForeignKey("exercise_table.id"), nullable=False)
    
    exercise = db.relationship('Exercise', back_populates="sets_and_reps")

class SetsRepsSchema(ma.Schema):
    
    # routine = fields.Nested('RoutineSchema', only=["name"])
    
    class Meta:
        # fields = ("id", "sets")
        fields = ("id", "sets", "reps", "exercise")
        # fields = ("routine")

set_rep_schema = SetsRepsSchema()
sets_reps_schema = SetsRepsSchema(many=True)