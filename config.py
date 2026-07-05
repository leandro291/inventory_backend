import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI=os.getenv('DB_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    CLOUDINARY_API_KEY=os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_CLOUD_NAME=os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_SECRET=os.getenv('CLOUDINARY_API_SECRET')