from marshmallow import fields
from init import db, ma


class Exercise(db.Model):
    __tablename__ = "exercise_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True) # have to catch error
    category = db.Column(db.String(30))
    muscles = db.Column(db.String(60))
    description = db.Column(db.Text)
    
    




class ExerciseSchema(ma.Schema):
    




    class Meta:
        fields = ("id", "name", "category", "muscles", "description")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)