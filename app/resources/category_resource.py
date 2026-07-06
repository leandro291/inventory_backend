from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.category_schema import CategorySchema
from app.services.category_service import category_service  

class CategoryResource(Resource):
    
    @jwt_required()
    def get(self):
        """
        Obtener todas las categorías
        ---
        tags:
          - Categorías
        responses:
          200:
            description: Lista de categorías obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_category:
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

            categories = category_service.get_all()
            categories_list = [category.to_json() for category in categories]
            return categories_list, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
        
    @jwt_required()
    def post(self):
        """
        Crear una nueva categoría
        ---
        tags:
          - Categorías
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
            description: Categoría creada exitosamente
            schema:
              type: object
              properties:
                id_category:
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
            description: La categoría ya existe o error de validación
        """
        try:
            
            data = request.get_json()
            validated_data = CategorySchema.model_validate(data)

            category = category_service.get_by_name(validated_data.name)

            if category:
                return {
                    'error': "category already exists"
                }, 400
            
            create_category = category_service.create(validated_data)

            return create_category.to_json(), 200
            
        except ValidationError as e:
            return {
                'error': str(e)
            }
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerCategoryResource(Resource):
    
    @jwt_required()
    def get(self, id_category: int):
        """
        Obtener una categoría por ID
        ---
        tags:
          - Categorías
        parameters:
          - in: path
            name: id_category
            type: integer
            required: true
            description: ID de la categoría
        responses:
          200:
            description: Categoría encontrada
            schema:
              type: object
              properties:
                id_category:
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
            description: Categoría no encontrada
        """
        try:
            
            category = category_service.get_by_id(id_category)

            if category is None:
                return {
                    'error': "category not found"
                }, 404
            
            return category.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_category: int):
        """
        Actualizar una categoría por ID
        ---
        tags:
          - Categorías
        parameters:
          - in: path
            name: id_category
            type: integer
            required: true
            description: ID de la categoría
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
            description: Categoría actualizada exitosamente
          400:
            description: Error de validación
          404:
            description: Categoría no encontrada
        """
        try:
            category = category_service.get_by_id(id_category)

            if category is None:
                return {
                    'error': "category not found"
                }, 404
            
            data = request.get_json()
            validated_data = CategorySchema.model_validate(data)
            update_category = category_service.update(category, validated_data)

            return update_category.to_json(), 200
        
        except ValidationError as e:
            return {
                'error': str(e)
            }
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_category: int):
        """
        Eliminar una categoría por ID
        ---
        tags:
          - Categorías
        parameters:
          - in: path
            name: id_category
            type: integer
            required: true
            description: ID de la categoría
        responses:
          200:
            description: Categoría eliminada exitosamente
          404:
            description: Categoría no encontrada
        """
        try:
            category = category_service.get_by_id(id_category)

            if category is None:
                return {
                    'error': "category not found"
                }, 404
            
            category_service.delete(category)

            return None, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
