from db import db
from app.models.user_model import User
from app.utils.helpers import crypto_helper
from app.utils.helpers import password_helper
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:

    def get_by_email(self, email: str) -> User | None:
        email = User.query.filter_by(email=email).first()
        return email
    
    def register(self, data: User) -> User:

        create_user = User(
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            password=password_helper.hash_password(data.password),
            id_role=data.id_role
        )

        db.session.add(create_user)
        db.session.commit()
        
        return create_user
    
    def login(self, user: User) -> User:

        hashed_id = crypto_helper.encrypt(user.id_user)

        access_token = create_access_token(
            identity=hashed_id,
            additional_claims={
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email
            }
        )

        refresh_token = create_refresh_token(
            identity=hashed_id
        )

        return access_token, refresh_token
    
    
auth_service = AuthService()