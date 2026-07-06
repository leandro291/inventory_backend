from db import db
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.inventory_schema import InventorySchema
from app.services.inventory_service import inventory_service


class InventoryResource(Resource):

    @jwt_required()
    def get(self):
        """
        Obtener todos los inventarios
        ---
        tags:
          - Inventarios
        responses:
          200:
            description: Lista de inventarios obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_inventory:
                    type: integer
                  stock:
                    type: integer
                  id_product:
                    type: integer
                  id_repository:
                    type: integer
                  is_active:
                    type: boolean
                  created_at:
                    type: string
                  updated_at:
                    type: string
          400:
            description: Error interno
        """
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
        """
        Crear o actualizar stock en inventario
        ---
        tags:
          - Inventarios
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                stock:
                  type: integer
                  example: 10
                id_product:
                  type: integer
                  example: 1
                id_repository:
                  type: integer
                  example: 1
              required:
                - stock
                - id_product
                - id_repository
        responses:
          200:
            description: Inventario creado o actualizado exitosamente
            schema:
              type: object
              properties:
                id_inventory:
                  type: integer
                stock:
                  type: integer
                id_product:
                  type: integer
                id_repository:
                  type: integer
                is_active:
                  type: boolean
                created_at:
                  type: string
                updated_at:
                  type: string
          400:
            description: Error de validación
        """
        try:
            data = request.get_json()
            validated_data = InventorySchema.model_validate(data)

            inventory = inventory_service.get_by_product_and_repository(
                validated_data.id_product,
                validated_data.id_repository,
            )

            if inventory:
                inventory.stock += validated_data.stock
                db.session.commit()
                return inventory.to_json(), 200

            inventory = inventory_service.create(validated_data)
            return inventory.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
                }, 400
        except Exception as e:
            return {
                'error': str(e)
                }, 400


class ManagerInventoryResource(Resource):

    @jwt_required()
    def get(self, id_inventory: int):
        """
        Obtener un inventario por ID
        ---
        tags:
          - Inventarios
        parameters:
          - in: path
            name: id_inventory
            type: integer
            required: true
            description: ID del inventario
        responses:
          200:
            description: Inventario encontrado
            schema:
              type: object
              properties:
                id_inventory:
                  type: integer
                stock:
                  type: integer
                id_product:
                  type: integer
                id_repository:
                  type: integer
                is_active:
                  type: boolean
                created_at:
                  type: string
                updated_at:
                  type: string
          404:
            description: Inventario no encontrado
        """
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
        """
        Actualizar un inventario por ID
        ---
        tags:
          - Inventarios
        parameters:
          - in: path
            name: id_inventory
            type: integer
            required: true
            description: ID del inventario
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                stock:
                  type: integer
                  example: 10
                id_product:
                  type: integer
                  example: 1
                id_repository:
                  type: integer
                  example: 1
              required:
                - stock
                - id_product
                - id_repository
        responses:
          200:
            description: Inventario actualizado exitosamente
          400:
            description: Error de validación
          404:
            description: Inventario no encontrado
        """
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
                'error': str(e.errors())
                }, 400
        except Exception as e:
            return {
                'error': str(e)
                }, 400

    @jwt_required()
    def delete(self, id_inventory: int):
        """
        Eliminar un inventario por ID
        ---
        tags:
          - Inventarios
        parameters:
          - in: path
            name: id_inventory
            type: integer
            required: true
            description: ID del inventario
        responses:
          200:
            description: Inventario eliminado exitosamente
          404:
            description: Inventario no encontrado
        """
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
