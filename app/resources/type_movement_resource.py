from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.type_movement_schema import TypeMovementSchema
from app.services.type_movement_service import type_movement_service

class TypeMovementResource(Resource):

    @jwt_required()
    def get(self):
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
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerTypeMovementResource(Resource):

    @jwt_required()
    def get(self, id_type_movement: int):
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
                'error': e.errors()
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_type_movement: int):
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
