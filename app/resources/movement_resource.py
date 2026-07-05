from db import db
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.movement_schema import MovementSchema
from app.services.movement_service import movement_service
from app.services.product_service import product_service
from app.services.inventory_service import inventory_service
from app.services.type_movement_service import type_movement_service
from app.services.movement_detail_service import movement_detail_service


class MovementResource(Resource):

    @jwt_required()
    def get(self):
        try:
            movements = movement_service.get_all()
            movements_list = [movement.to_json() for movement in movements]
            return movements_list, 200
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validated_data = MovementSchema.model_validate(data)

            type_movement = type_movement_service.get_by_id(
                validated_data.id_type_movement
            )

            if type_movement is None:
                return {
                    'error': 'type movement not found'
                    }, 404

            is_entry = type_movement.name.lower() == 'entrada'

            movement = movement_service.create(validated_data)
            db.session.flush()

            for item in validated_data.movement_details:
                product = product_service.get_by_id(item.id_product)

                if product is None:
                    raise Exception(f'product {item.id_product} not found')

                inventory = inventory_service.get_by_product_and_repository(
                    item.id_product,
                    validated_data.id_repository,
                )

                if inventory is None:
                    raise Exception(
                        f'product {item.id_product} has no inventory in this repository'
                    )

                movement_detail_service.create(item, movement.id_movement)

                if is_entry:
                    inventory.stock += item.quantity
                else:
                    if inventory.stock < item.quantity:
                        raise Exception(
                            f'insufficient stock for product {item.id_product}'
                        )
                    inventory.stock -= item.quantity

            db.session.commit()

            return movement.to_json(), 201

        except ValidationError as e:
            return {
                'error': str(e.errors())
                }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
                }, 400


class ManagerMovementResource(Resource):

    @jwt_required()
    def get(self, id_movement: int):
        try:
            movement = movement_service.get_by_id(id_movement)

            if movement is None:
                return {
                    'error': 'movement not found'
                    }, 404
            
            return movement.to_json(), 200
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def delete(self, id_movement: int):
        try:
            movement = movement_service.get_by_id(id_movement)

            if movement is None:
                return {
                    'error': 'movement not found'
                    }, 404
            
            movement_service.delete(movement)

            return None, 200
        except Exception as e:
            return {
                'error': str(e)
                }, 400
