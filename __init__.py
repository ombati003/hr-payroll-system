from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import main_bp
    from app.routes.main_fe import main_fe_bp
    from app.routes.employees import employees_bp
    from app.routes.leave import leave_bp
    from app.routes.payroll import payroll_bp

    app.register_blueprint(main_fe_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(leave_bp, url_prefix='/api/leave')
    app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

    return app
