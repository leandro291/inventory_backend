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
        """
        Obtener todos los productos
        ---
        tags:
          - Productos
        responses:
          200:
            description: Lista de productos obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_product:
                    type: integer
                  code:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
                  image:
                    type: string
                  brand:
                    type: string
                  purchase_price:
                    type: number
                  sale_price:
                    type: number
                  status:
                    type: boolean
                  created_at:
                    type: string
                  updated_at:
                    type: string
                  id_category:
                    type: integer
          400:
            description: Error interno
        """
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
        """
        Crear un nuevo producto (multipart/form-data)
        ---
        tags:
          - Productos
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: image
            type: file
            required: true
            description: Imagen del producto
          - in: formData
            name: name
            type: string
            required: true
            description: Nombre del producto
          - in: formData
            name: description
            type: string
            required: true
            description: Descripción del producto
          - in: formData
            name: brand
            type: string
            required: true
            description: Marca del producto
          - in: formData
            name: purchase_price
            type: number
            required: true
            description: Precio de compra
          - in: formData
            name: sale_price
            type: number
            required: true
            description: Precio de venta
          - in: formData
            name: id_category
            type: integer
            required: true
            description: ID de la categoría
        responses:
          200:
            description: Producto creado exitosamente
            schema:
              type: object
              properties:
                id_product:
                  type: integer
                code:
                  type: string
                name:
                  type: string
                description:
                  type: string
                image:
                  type: string
                brand:
                  type: string
                purchase_price:
                  type: number
                sale_price:
                  type: number
                status:
                  type: boolean
                created_at:
                  type: string
                updated_at:
                  type: string
                id_category:
                  type: integer
          400:
            description: Error de validación
          404:
            description: Error al subir la imagen
        """
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
        """
        Obtener un producto por ID
        ---
        tags:
          - Productos
        parameters:
          - in: path
            name: id_product
            type: integer
            required: true
            description: ID del producto
        responses:
          200:
            description: Producto encontrado
            schema:
              type: object
              properties:
                id_product:
                  type: integer
                code:
                  type: string
                name:
                  type: string
                description:
                  type: string
                image:
                  type: string
                brand:
                  type: string
                purchase_price:
                  type: number
                sale_price:
                  type: number
                status:
                  type: boolean
                created_at:
                  type: string
                updated_at:
                  type: string
                id_category:
                  type: integer
          404:
            description: Producto no encontrado
        """
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
        """
        Actualizar un producto por ID (multipart/form-data)
        ---
        tags:
          - Productos
        consumes:
          - multipart/form-data
        parameters:
          - in: path
            name: id_product
            type: integer
            required: true
            description: ID del producto
          - in: formData
            name: image
            type: file
            required: false
            description: Imagen del producto
          - in: formData
            name: name
            type: string
            required: true
            description: Nombre del producto
          - in: formData
            name: description
            type: string
            required: true
            description: Descripción del producto
          - in: formData
            name: brand
            type: string
            required: true
            description: Marca del producto
          - in: formData
            name: purchase_price
            type: number
            required: true
            description: Precio de compra
          - in: formData
            name: sale_price
            type: number
            required: true
            description: Precio de venta
          - in: formData
            name: id_category
            type: integer
            required: true
            description: ID de la categoría
        responses:
          200:
            description: Producto actualizado exitosamente
          400:
            description: Error de validación
          404:
            description: Producto no encontrado o error al subir imagen
        """
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
        """
        Eliminar un producto por ID
        ---
        tags:
          - Productos
        parameters:
          - in: path
            name: id_product
            type: integer
            required: true
            description: ID del producto
        responses:
          200:
            description: Producto eliminado exitosamente
          404:
            description: Producto no encontrado
        """
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