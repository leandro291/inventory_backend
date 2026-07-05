from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.product_schema import ProductSchema
from app.utils.helpers import cloudinary_helper
from app.services.product_service import product_service

class ProductResource(Resource):

    @jwt_required()
    def get(self):

        try:
            products = product_service.get_all()
            products_list = []

            for product in products:
                secure_url = cloudinary_helper.get_secure_url(product.image)
                product.image = secure_url
                products_list.append(product.to_json())

            return products_list, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
    @jwt_required()
    def post(self):
        try:
            data = request.form
            image = request.files.get('image')

            cloudinary_helper.validate_image(image)

            validated_data = ProductSchema.model_validate(data)

            secure_url, public_id = cloudinary_helper.upload_image(image, "products")

            if not secure_url:
                return {
                    'error': 'error uploading image'
                }, 404
            
            next_code = 'P-00001'
            product = product_service.get_last()
            
            if product:
                code = product.code
                next_code = 'P-' + str(int(code.split('-')[1]) + 1).zfill(5)

            created_product = product_service.create(
                validated_data,
                next_code,
                public_id
            )

            created_product.image = secure_url

            return created_product.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerProductResource(Resource):
    @jwt_required()
    def get(self, id_product: int):
        try:
            product = product_service.get_by_id(id_product)

            if product is None:
                return {
                    'error': 'product not found'
                }, 404
            
            secure_url = cloudinary_helper.get_secure_url(product.image)
            product.image = secure_url
            return product.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
    @jwt_required()
    def put(self, id_product: int):
        try:
            data = request.form
            validated_data = ProductSchema.model_validate(data)

            product = product_service.get_by_id(id_product)

            if product is None:
                return {
                    'error': 'product not found'
                }, 404
            
            image = request.files.get('image')

            if image:
                cloudinary_helper.validate_image(image)

                secure_url, error = cloudinary_helper.upload_image(image, 'products')
                cloudinary_helper.delete_image(product.image)

                if not secure_url:
                    return {
                        'error': f'error uploading image: {error}'
                    }, 404

                public_id = error
                
                updated_product = product_service.update(validated_data, product, public_id)
                updated_product.image = secure_url
            else:
                updated_product = product_service.update(validated_data, product, None)
                updated_product.image = cloudinary_helper.get_secure_url(updated_product.image)

            return updated_product.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
    @jwt_required()
    def delete(self, id_product: int):
        try:
            product = product_service.get_by_id(id_product)

            if product is None:
                return {
                    'error': 'product not found'
                }, 404
            
            deleted_product = product_service.delete(product)
            return None, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400