from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)

    # Import routes (circular import avoid karne ke liye)
    from app.routes.books import books_bp
    app.register_blueprint(books_bp, url_prefix='/api')

    # Create tables
    with app.app_context():
        db.create_all()

    return app