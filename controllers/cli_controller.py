from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create_tables")
def create_tables():
    db.create_all()
    print("Tables created")
    
@db_commands.cli.command("drop_tables")
def drop_tables():
    db.drop_all()
    print("Tables dropped")
    
@db_commands.cli.command("seed_tables")
def seed_tables():
    user = [
        User(
            name = "The Admin",
            email = "admin@workout_webAPI.com",
            password = bcrypt.generate_password_hash('1234').decode('utf-8'),
            date_joined = "",
            age = "",
            weight = "",
            height = "",
            gender = "",
            is_admin = True
        ),
        User(
            name = "Gustavo Jimenez",
            email = "gus.jim@workout_webAPI.com",
            password = bcrypt.generate_password_hash('1234').decode('utf-8'),
            date_joined = "February",
            age = "43",
            weight = "68",
            height = "170",
            gender = "1"
        )
    ]
    
    db.session.add_all(user)
    db.session.commit() 
    
    print("Tables seeded")