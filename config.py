import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:Dc2025@localhost/affirmationdb")  # Replace with your DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
