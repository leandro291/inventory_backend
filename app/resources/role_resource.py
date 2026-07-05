from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.models.role_model import Role
from app.schemas.role_schema import RoleSchema
from app.services.role_service import role_service

class RoleResource(Resource):
    
    def get(self):
        
        try:

            roles: list[Role] = role_service.get_all()
            roles_list = [role.to_json() for role in roles]
            return roles_list, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
    @jwt_required()
    def post(self):
        try:

            data = request.get_json()
            validated_data = RoleSchema.model_validate(data)

            name = role_service.get_by_name(validated_data.name)

            if name:
                return {
                    'error': 'role already exists'
                }, 400

            created_role = role_service.create(validated_data)

            return created_role.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400


class ManagerRoleResource(Resource):

    def get(self, id_role: int):
        try:
            
            role: Role = role_service.get_by_id(id_role)

            if role is None:
                return {
                    'error': "role not found"
                }, 404
            
            return role.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_role: int):
        try:

            role: Role = role_service.get_by_id(id_role)

            if role is None:
                return {
                    'error': "role not found"
                }, 404

            data = request.get_json()
            validated_data = RoleSchema.model_validate(data)

            name = role_service.get_by_name(validated_data.name)

            if name:
                return {
                    'error': 'role already exists'
                }, 400
            
            role = role_service.update(role, validated_data)

            return role.to_json(), 200
        
        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_role: int):
        try:

            role: Role = role_service.get_by_id(id_role)

            if role is None:
                return {
                    'error': "role not found"
                }, 404
            
            role_service.delete(role)

            return None, 200
            
        except Exception as e:
            return {
                'error': str(e)
            }, 400
