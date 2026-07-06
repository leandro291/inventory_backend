from db import db
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Inventario Flask",
        "description": "API de inventario y productos",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
        },
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header usando el esquema Bearer. Ejemplo: 'Bearer {token}'",
        }
    },
    "security": [{"Bearer": []}],
})

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