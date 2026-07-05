from flask import request
from flask_restful import Resource
from pydantic import ValidationError
from app.utils.helpers import password_helper
from app.services.auth_servivce import auth_service
from app.schemas.auth_schema import LoginSchema, RegisterSchema

class LoginResource(Resource):

    def post(self):
        try:
            data = request.get_json()
            validated_data = LoginSchema.model_validate(data)

            user = auth_service.get_by_email(validated_data.email)

            if user is None:
                return {
                    'error': 'email nout found'
                }, 401
            
            is_password_valid = password_helper.verify_password(validated_data.password, user.password)

            if not is_password_valid:
                return {
                    'error': 'user nout found'
                }, 401
            
            access_token, refresh_token = auth_service.login(user)

            return {
                'access': access_token,
                'refresh': refresh_token
            }, 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class RegisterResource(Resource):

    def post(self):
        try:
            data = request.get_json()
            validated_data = RegisterSchema.model_validate(data)

            user = auth_service.get_by_email(validated_data.email)

            if user:
                return {
                    'error': 'email alredy exists'
                }, 404
            
            create_user = auth_service.register(validated_data)

            return create_user.to_json(), 200
            
        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 404
        except Exception as e:
            return {
                'error': str(e)
            }, 400