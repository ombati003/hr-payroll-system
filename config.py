import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    # Defaulting to a local sqlite for development if postgres is not ready, 
    # but the requirement is postgres.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/hr_payroll'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
