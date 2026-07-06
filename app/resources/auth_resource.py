from flask import request
from flask_restful import Resource
from pydantic import ValidationError
from app.utils.helpers import password_helper
from app.services.auth_servivce import auth_service
from app.schemas.auth_schema import LoginSchema, RegisterSchema

class LoginResource(Resource):

    def post(self):
        """
        Iniciar sesión
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: "user@example.com"
                password:
                  type: string
                  example: "password123"
              required:
                - email
                - password
        responses:
          200:
            description: Inicio de sesión exitoso
            schema:
              type: object
              properties:
                access:
                  type: string
                refresh:
                  type: string
          400:
            description: Error de validación
          401:
            description: Credenciales inválidas
        """
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
        """
        Registrar un nuevo usuario
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Leandro"
                last_name:
                  type: string
                  example: "Rojas"
                email:
                  type: string
                  example: "leandro@example.com"
                password:
                  type: string
                  example: "password123"
                id_role:
                  type: integer
                  example: 1
              required:
                - name
                - last_name
                - email
                - password
                - id_role
        responses:
          200:
            description: Usuario creado exitosamente
            schema:
              type: object
              properties:
                id_user:
                  type: integer
                name:
                  type: string
                last_name:
                  type: string
                email:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
                id_role:
                  type: integer
          400:
            description: Error de validación
          404:
            description: El email ya existe
        """
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