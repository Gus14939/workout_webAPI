from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

from init import db, ma

DIFFICULTY = ("Beginner", "Easy", "Medium", "Hard", "Advanced")

class Exercise(db.Model):
    __tablename__ = "exercise_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    category = db.Column(db.String(20))
    muscles = db.Column(db.String(60))
    description = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey("routine_table.id"), nullable=False)
    
    user = db.relationship('User', back_populates="exercises")
    routine = db.relationship('Routine', back_populates="exercises")
    sets_reps = db.relationship("SetsReps", back_populates="exercises", cascade="all, delete")

class ExerciseSchema(ma.Schema):
    
    # Validation
    name = fields.String(validate=And(
        Length(min=3, max=24, error="The name should be 3 to 24 characters"),
        Regexp('^[A-Za-z0-9 -_+,]+$', error="Only Alphanumeric characters, dashes, underscore, plus sign, and coma")
    ))
        
    category = fields.String(validate=OneOf(DIFFICULTY))
    
    muscles = fields.String(validate=Length(max=60, error="Muscles involved in the work-out should not be longer than 60 characters long"))  
      
    description = fields.String(validate=Length(min=10, max=128, error="Exercise description should be between 10 and 128 characters long"))    
    
    user = fields.Nested('UserSchema', only=["name"])
    routine = fields.Nested('RoutineSchema', only=["weekday", "name"])
    sets_reps = fields.List(fields.Nested('SetsRepsSchema', only=["id", "sets", "reps", "goal"]))
    
    class Meta:
        # fields = ("id", "name", "category", "muscles", "description", "routine", "user")
        fields = ("id", "name", "category", "muscles", "description", "user", "routine", "sets_reps")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
