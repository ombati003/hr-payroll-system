import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7777@localhost:5432/hr_payroll"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
