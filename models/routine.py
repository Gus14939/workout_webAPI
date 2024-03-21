from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

class Routine(db.Model):
    __tablename__ = "routine_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False, unique=True) # have to catch error
    description = db.Column(db.String(128))
    weekday = db.Column(db.String(10))
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), nullable=False)

    user = db.relationship('User', back_populates="routines")
    exercises = db.relationship('Exercise', back_populates="routine", cascade='all, delete')
    
class RoutineSchema(ma.Schema):
    
    # Validation
    name = fields.String(validate=And(
        Length(min=3, max=24, error="The name should be 3 to 24 characters"),
        Regexp('^[A-Za-z0-9 -_+,]+$', error="Only Alphanumeric characters, dashes, underscore, plus sign, and coma")
    ))
    # 2 names cannot be the same
    @validates("name")
    def same_name(self, new_routine_name):
        existing_routine_name = db.session.query(Routine).filter_by(name=new_routine_name).first()
        if existing_routine_name:
            raise ValidationError(f"There's a routine named '{new_routine_name}' already. Assign a different name")
        
    description = fields.String(validate=Length(min=10, max=128, error="Routine description should be between 10 and 128 characters long"))
    
    weekday = fields.String(validate=OneOf(WEEKDAYS, error="Must be the full name of a day of the week"))
    
    # only one Routine per day
    @validates("weekday")
    def validate_one_routine_per_day(self, routine_day):
        if routine_day in WEEKDAYS:
            index_of_routine_day_in_WEEKDAYS = WEEKDAYS.index(routine_day)
            stmt = db.select(db.func.count()).select_from(Routine).filter_by(weekday=WEEKDAYS[index_of_routine_day_in_WEEKDAYS])
            routines_in_day_count = db.session.scalar(stmt)
            if routines_in_day_count > 0:
                raise ValidationError(f"There's a routine for {routine_day} already. Only one routine per day")
    
    user = fields.Nested('UserSchema', exclude=["password", "email", "is_admin", "date_joined", "routines", "exercises", "sets_reps"])
    exercises = fields.List(fields.Nested('ExerciseSchema', exclude=["routine"]))
    
    class Meta:
        fields = ("id", "name", "description", "weekday", "user", "exercises")
        
routine_schema = RoutineSchema()
routines_schema = RoutineSchema(many=True)