from marshmallow import fields
from init import db, ma


class Routine(db.Model):
    __tablename__ = "routine_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    description = db.Column(db.Text)
    weekday = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)
    
    user = db.relationship('User', back_populates="routine_table")
    
class RoutineSchema(ma.Schema):
    
    user = fields.Nested('UserSchema', only = ["name"])
    
    class Meta:
        fields = ("id", "name", "description", "weekday", "users")
        
routine_schema = RoutineSchema()
routines_schema = RoutineSchema(many=True)