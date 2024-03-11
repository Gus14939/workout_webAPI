from marshmallow import fields
from init import db, ma


class Exercise(db.Model):
    __tablename__ = "exercise_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True) # have to catch error
    category = db.Column(db.String(30))
    muscles = db.Column(db.String(60))
    description = db.Column(db.Text)
    
    # user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    
    # user = db.relationship('User', back_populates="exercises")

class ExerciseSchema(ma.Schema):
    
    # user = fields.Nested('UserSchema', only=["name"])
    
    class Meta:
        fields = ("id", "name", "category", "muscles", "description")
        # fields = ("id", "name", "category", "muscles", "description", "user")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)