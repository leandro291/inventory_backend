from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.type_movement_schema import TypeMovementSchema
from app.services.type_movement_service import type_movement_service

class TypeMovementResource(Resource):

    @jwt_required()
    def get(self):
        """
        Obtener todos los tipos de movimiento
        ---
        tags:
          - Tipos de Movimiento
        responses:
          200:
            description: Lista de tipos de movimiento obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_type_movement:
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
            type_movements = type_movement_service.get_all()
            type_movements_list = [tm.to_json() for tm in type_movements]
            return type_movements_list, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def post(self):
        """
        Crear un nuevo tipo de movimiento
        ---
        tags:
          - Tipos de Movimiento
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
            description: Tipo de movimiento creado exitosamente
            schema:
              type: object
              properties:
                id_type_movement:
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
            description: El nombre ya existe o error de validación
        """
        try:
            data = request.get_json()
            validated_data = TypeMovementSchema.model_validate(data)

            type_movement = type_movement_service.get_by_name(validated_data.name)

            if type_movement:
                return {
                    'error': "type movement name already exists"
                }, 400

            create_type_movement = type_movement_service.create(validated_data)

            return create_type_movement.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerTypeMovementResource(Resource):

    @jwt_required()
    def get(self, id_type_movement: int):
        """
        Obtener un tipo de movimiento por ID
        ---
        tags:
          - Tipos de Movimiento
        parameters:
          - in: path
            name: id_type_movement
            type: integer
            required: true
            description: ID del tipo de movimiento
        responses:
          200:
            description: Tipo de movimiento encontrado
            schema:
              type: object
              properties:
                id_type_movement:
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
            description: Tipo de movimiento no encontrado
        """
        try:
            type_movement = type_movement_service.get_by_id(id_type_movement)

            if type_movement is None:
                return {
                    'error': "type movement not found"
                }, 404

            return type_movement.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_type_movement: int):
        """
        Actualizar un tipo de movimiento por ID
        ---
        tags:
          - Tipos de Movimiento
        parameters:
          - in: path
            name: id_type_movement
            type: integer
            required: true
            description: ID del tipo de movimiento
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
            description: Tipo de movimiento actualizado exitosamente
          400:
            description: El nombre ya existe o error de validación
          404:
            description: Tipo de movimiento no encontrado
        """
        try:
            type_movement = type_movement_service.get_by_id(id_type_movement)

            if type_movement is None:
                return {
                    'error': "type movement not found"
                }, 404

            data = request.get_json()
            validated_data = TypeMovementSchema.model_validate(data)

            type_movement = type_movement_service.get_by_name(validated_data.name)
            if type_movement :
                return {
                    'error': "type movement name already exists"
                }, 400

            update_type_movement = type_movement_service.update(type_movement, validated_data)

            return update_type_movement.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_type_movement: int):
        """
        Eliminar un tipo de movimiento por ID
        ---
        tags:
          - Tipos de Movimiento
        parameters:
          - in: path
            name: id_type_movement
            type: integer
            required: true
            description: ID del tipo de movimiento
        responses:
          200:
            description: Tipo de movimiento eliminado exitosamente
          404:
            description: Tipo de movimiento no encontrado
        """
        try:
            type_movement = type_movement_service.get_by_id(id_type_movement)

            if type_movement is None:
                return {
                    'error': "type movement not found"
                }, 404

            type_movement_service.delete(type_movement)

            return None, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
