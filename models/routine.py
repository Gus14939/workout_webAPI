from marshmallow import fields
from init import db, ma


class Routine(db.Model):
    __tablename__ = "routine_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False, unique=True) # have to catch error
    description = db.Column(db.Text)
    weekday = db.Column(db.String(10))
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)

    user = db.relationship('User', back_populates="routines")
    exercises = db.relationship('Exercise', back_populates="routine", cascade='all, delete')
    
class RoutineSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only=["name"])
    exercises = fields.List(fields.Nested('ExerciseSchema', exclude=["user"]))
    
    class Meta:
        fields = ("id", "name", "description", "weekday", "user", "exercises")
        
routine_schema = RoutineSchema()
routines_schema = RoutineSchema(many=True)