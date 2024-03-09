from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.routine import Routine

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
    users = [
        User(
            name = "The Admin",
            email = "admin@workoutwebAPI.com",
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
            email = "gus.jim@workoutwebAPI.com",
            password = bcrypt.generate_password_hash('1234').decode('utf-8'),
            date_joined = "February",
            age = "43",
            weight = "68",
            height = "170",
            gender = "1"
        )
    ]
    db.session.add_all(users)
    
    routines = [
        Routine(
            name = "Chest",
            description = "La descripcion para pecho",
            weekday = 1,
            user = users[0]
        ),
        Routine(
            name = "Legs",
            description = "La descripcion para piernas",
            weekday = 2,
            user = users[1]
        ),
        Routine(
            name = "Arms",
            description = "La descripcion para los brazos",
            weekday = 3,
            user = users[1]
        ),
        Routine(
            name = "Back",
            description = "La descripcion de ejercicios para espalda",
            weekday = 4,
            user = users[1]
        )
    ]
    db.session.add_all(routines)
    
    db.session.commit() 
    
    print("Tables seeded")