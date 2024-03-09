from init import db, ma

class User(db.Model):
    __tablename__ = "user_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    weight = db.Column(db.String, nullable=False)
    height = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "date_joined", "age", "weight", "height", "gender", "is_admin")
        

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
        
        