from datetime import date
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.routine import Routine
from models.exercise import Exercise
from models.sets_reps import SetsReps

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
            date_joined = date.today(),
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
            date_joined = date.today(),
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
            description = "Description for Chest workout",
            weekday = "Monday",
            user = users[1]
        ),
        Routine(
            name = "Legs",
            description = "Description for Legs exercises",
            weekday = "Tuesday",
            user = users[1]
        ),
        Routine(
            name = "Arms",
            description = "Description of the best Arms exercises",
            weekday = "Wednesday",
            user = users[0]
        ),
        Routine(
            name = "Back",
            description = "Description Back",
            weekday = "Thursday",
            user = users[0]
        )
    ]
    db.session.add_all(routines)
    
    exercises = [
        Exercise(
            name = "Bench Press",
            category = "easy",
            muscles = "Pectoralis major, Anterior deltoids, Triceps brachii",
            description = "Description Bench Press",
            user = users[1],
            routine = routines[0]
        ),
        Exercise(
            name = "Push-Ups",
            category = "easy",
            muscles = "Pectoralis major, Anterior deltoids, Triceps brachii",
            description = "Description Push-Ups",
            user = users[1],
            routine = routines[0]
        ),
        Exercise(
            name="Leg Press",
            category="easy",
            muscles="Quadriceps, Hamstrings, Glutes",
            description="Sit on the leg press machine with your feet shoulder-width apart on the footplate.",
            user = users[1],
            routine = routines[1]
        )
    ]
    db.session.add_all(exercises)   
    
    set_and_reps = [
        SetsReps(
            sets = "4",
            reps = "10",
            user = users[1],
            # exercise = exercises[0]
        ), 
        SetsReps(
            sets = "3",
            reps = "20",
            user = users[1],
            # exercise = exercises[1]
        )
    ]
    db.session.add_all(set_and_reps)   
    
    db.session.commit() 
    
    print("Tables seeded")
