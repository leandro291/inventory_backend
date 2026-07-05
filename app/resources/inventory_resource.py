from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.inventory_schema import InventorySchema
from app.services.inventory_service import inventory_service


class InventoryResource(Resource):

    @jwt_required()
    def get(self):
        try:
            inventories = inventory_service.get_all()
            inventories_list = [inventory.to_json() for inventory in inventories]
            return inventories_list, 200
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validated_data = InventorySchema.model_validate(data)

            inventory = inventory_service.get_by_product_and_repository(
                validated_data.id_product,
                validated_data.id_repository,
            )

            if inventory:
                return {
                    'error': 'inventory already exists for this product and repository'
                }, 400

            inventory = inventory_service.create(validated_data)
            return inventory.to_json(), 200

        except ValidationError as e:
            return {
                'error': e.errors()
                }, 400
        except Exception as e:
            return {
                'error': str(e)
                }, 400


class ManagerInventoryResource(Resource):

    @jwt_required()
    def get(self, id_inventory: int):
        try:
            inventory = inventory_service.get_by_id(id_inventory)
            if inventory is None:
                return {
                    'error': 'inventory not found'
                    }, 404
            return inventory.to_json(), 200
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def put(self, id_inventory: int):
        try:
            inventory = inventory_service.get_by_id(id_inventory)
            if inventory is None:
                return {
                    'error': 'inventory not found'
                    }, 404

            data = request.get_json()
            validated_data = InventorySchema.model_validate(data)
            inventory = inventory_service.update(inventory, validated_data)
            return inventory.to_json(), 200

        except ValidationError as e:
            return {
                'error': e.errors()
                }, 400
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def delete(self, id_inventory: int):
        try:
            inventory = inventory_service.get_by_id(id_inventory)

            if inventory is None:
                return {
                    'error': 'inventory not found'
                    }, 404
            inventory_service.delete(inventory)

            return None, 200
        
        except Exception as e:
            return {
                'error': str(e)
                }, 400
