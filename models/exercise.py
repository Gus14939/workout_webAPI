from marshmallow import fields
from init import db, ma


class Exercise(db.Model):
    __tablename__ = "exercise_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True) # have to catch error
    category = db.Column(db.String(30))
    muscles = db.Column(db.String(60))
    description = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    sets_and_reps_id = db.Column(db.Integer, db.ForeignKey("sets_and_reps_table.id"), nullable=False)
    
    
    user = db.relationship('User', back_populates="exercises")
    sets_and_reps = db.relationship("SetsReps", back_populates="exercise", cascade="all, delete")

class ExerciseSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only=["name"])
    sets_and_reps = fields.Nested('SetsRepsSchema', only=["sets", "reps"])
    
    class Meta:
        # fields = ("id", "name", "category", "muscles", "description", "user")
        fields = ("id", "name", "category", "muscles", "description", "user", "sets_and_reps")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)