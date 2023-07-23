from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/toy_library_development'

    db.init_app(app)
    migrate.init_app(app, db)

    
    from app.models.user import User
    from app.models.toy import Toy
    from app.models.transaction import Transaction
        # from .models.hold import hold_toys
        # from .models.checked_out_history import CheckedOutHistory

    # users_toys = db.Table('users_toys',
    #         db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    #         db.Column('toy_id', db.Integer, db.ForeignKey('toy.toy_id')),
    #         db.Column('status', db.String)
        # )

    from app.user_routes import users_bp
    app.register_blueprint(users_bp)

    from app.toy_routes import toys_bp
    app.register_blueprint(toys_bp)


    return app