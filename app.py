from flask import Flask

from api.routes import bp
from api.student import students_bp
from database import migrate, db
from settings import settings
# Import models so metadata is registered
from models.sqlalchemy.student import Student


def create_app():
    app = Flask(__name__)
    # Load DB URL from .env (via pydantic BaseSettings)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(bp)
    app.register_blueprint(students_bp)

    # Create all tables (ensure model imports before this)
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run(debug=True)