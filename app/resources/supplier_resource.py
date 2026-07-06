from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.supplier_schema import SupplierSchema
from app.services.supplier_service import supplier_service

class SupplierResource(Resource):

    @jwt_required()
    def get(self):
        """
        Obtener todos los proveedores
        ---
        tags:
          - Proveedores
        responses:
          200:
            description: Lista de proveedores obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_supplier:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
                  telephone:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
                  id_company:
                    type: integer
          400:
            description: Error interno
        """
        try:
            suppliers = supplier_service.get_all()
            suppliers_list = [supplier.to_json() for supplier in suppliers]
            return suppliers_list, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def post(self):
        """
        Crear un nuevo proveedor
        ---
        tags:
          - Proveedores
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
                email:
                  type: string
                  example: "proveedor@example.com"
                telephone:
                  type: string
                  example: "999999999"
                id_company:
                  type: integer
                  example: 1
              required:
                - name
                - email
                - telephone
                - id_company
        responses:
          200:
            description: Proveedor creado exitosamente
            schema:
              type: object
              properties:
                id_supplier:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                telephone:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
                id_company:
                  type: integer
          400:
            description: El email ya existe o error de validación
        """
        try:
            data = request.get_json()
            validated_data = SupplierSchema.model_validate(data)
            
            supplier = supplier_service.get_by_email(email=validated_data.email)

            if supplier:
                return {
                    'error': "email already exists"
                }, 400
            
            create_supplier = supplier_service.create(validated_data)

            return create_supplier.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerSupplierResource(Resource):

    @jwt_required()
    def get(self, id_supplier: int):
        """
        Obtener un proveedor por ID
        ---
        tags:
          - Proveedores
        parameters:
          - in: path
            name: id_supplier
            type: integer
            required: true
            description: ID del proveedor
        responses:
          200:
            description: Proveedor encontrado
            schema:
              type: object
              properties:
                id_supplier:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                telephone:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
                id_company:
                  type: integer
          404:
            description: Proveedor no encontrado
        """
        try:
            supplier = supplier_service.get_by_id(id_supplier)

            if supplier is None:
                return {
                    'error': "supplier not found"
                }, 404

            return supplier.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_supplier: int):
        """
        Actualizar un proveedor por ID
        ---
        tags:
          - Proveedores
        parameters:
          - in: path
            name: id_supplier
            type: integer
            required: true
            description: ID del proveedor
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "string"
                email:
                  type: string
                  example: "proveedor@example.com"
                telephone:
                  type: string
                  example: "999999999"
                id_company:
                  type: integer
                  example: 1
              required:
                - name
                - email
                - telephone
                - id_company
        responses:
          200:
            description: Proveedor actualizado exitosamente
          400:
            description: El email ya existe o error de validación
          404:
            description: Proveedor no encontrado
        """
        try:
            supplier = supplier_service.get_by_id(id_supplier)

            if supplier is None:
                return {
                    'error': "supplier not found"
                }, 404

            data = request.get_json()
            validated_data = SupplierSchema.model_validate(data)

            supplier = supplier_service.get_by_email(validated_data.email)

            if supplier:
                return {
                    'error': "email already exists"
                }, 400

            update_supplier = supplier_service.update(supplier, validated_data)

            return update_supplier.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_supplier: int):
        """
        Eliminar un proveedor por ID
        ---
        tags:
          - Proveedores
        parameters:
          - in: path
            name: id_supplier
            type: integer
            required: true
            description: ID del proveedor
        responses:
          200:
            description: Proveedor eliminado exitosamente
          404:
            description: Proveedor no encontrado
        """
        try:
            supplier = supplier_service.get_by_id(id_supplier)

            if supplier is None:
                return {
                    'error': "supplier not found"
                }, 404

            supplier_service.delete(supplier)

            return None, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400