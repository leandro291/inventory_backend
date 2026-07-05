from db import db
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.models import (
    role_model,
    user_model,
    company_model,
    product_model,
    movement_model,
    category_model,
    supplier_model,
    inventory_model,
    repository_model,
    type_movement_model
)

from app import router