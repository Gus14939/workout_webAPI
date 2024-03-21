import os
from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    
    app.json.sort_keys = False
    
    # config
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    
    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Error handling 
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": "Not found"}, 404
    
    # Add CLI commands
    
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    
    from controllers.user_controller import profile_bp
    app.register_blueprint(profile_bp)
    
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    
    from controllers.routine_controller import routine_bp
    app.register_blueprint(routine_bp)
    
    # blueprint for exercise only
    from controllers.exercise_controller import exercise_only_bp
    app.register_blueprint(exercise_only_bp)
    
    # from controllers.sets_reps_controller import sets_reps_bp
    # app.register_blueprint(sets_reps_bp)
    #
    return app