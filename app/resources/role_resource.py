from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.models.role_model import Role
from app.schemas.role_schema import RoleSchema
from app.services.role_service import role_service

class RoleResource(Resource):

    def get(self):
        """
        Obtener todos los roles
        ---
        tags:
          - Roles
        responses:
          200:
            description: Lista de roles obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_role:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
          400:
            description: Error interno
        """
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
        """
        Crear un nuevo rol
        ---
        tags:
          - Roles
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "string"
                description:
                  type: string
                  example: "string"
              required:
                - name
                - description
        responses:
          200:
            description: Rol creado exitosamente
            schema:
              type: object
              properties:
                id_role:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          400:
            description: El rol ya existe o error de validación
        """
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
        """
        Obtener un rol por ID
        ---
        tags:
          - Roles
        parameters:
          - in: path
            name: id_role
            type: integer
            required: true
            description: ID del rol
        responses:
          200:
            description: Rol encontrado
            schema:
              type: object
              properties:
                id_role:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          404:
            description: Rol no encontrado
        """
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
        """
        Actualizar un rol por ID
        ---
        tags:
          - Roles
        parameters:
          - in: path
            name: id_role
            type: integer
            required: true
            description: ID del rol
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "string"
                description:
                  type: string
                  example: "string"
              required:
                - name
                - description
        responses:
          200:
            description: Rol actualizado exitosamente
          400:
            description: El rol ya existe o error de validación
          404:
            description: Rol no encontrado
        """
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
        """
        Eliminar un rol por ID
        ---
        tags:
          - Roles
        parameters:
          - in: path
            name: id_role
            type: integer
            required: true
            description: ID del rol
        responses:
          200:
            description: Rol eliminado exitosamente
          404:
            description: Rol no encontrado
        """
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
