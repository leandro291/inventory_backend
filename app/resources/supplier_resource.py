from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.supplier_schema import SupplierSchema
from app.services.supplier_service import supplier_service

class SupplierResource(Resource):

    @jwt_required()
    def get(self):
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