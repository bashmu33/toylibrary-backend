from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/users/*": {"origins": ["http://localhost:3000", "https://fw-toy-library-b75c4b0033c3.herokuapp.com"]}})

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("RENDER_DATABASE_URI")


    db.init_app(app)
    migrate.init_app(app, db)

    
    from app.models.user import User
    from app.models.toy import Toy
    from app.models.transaction import Transaction

    from app.user_routes import users_bp
    app.register_blueprint(users_bp)

    from app.toy_routes import toys_bp
    app.register_blueprint(toys_bp)

    from app.transaction_routes import transactions_bp
    app.register_blueprint(transactions_bp)


    return app