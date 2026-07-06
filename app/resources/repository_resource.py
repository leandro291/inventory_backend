from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.repository_schema import RepositorySchema
from app.services.repository_service import repository_service

class RepositoryResource(Resource):

    @jwt_required()
    def get(self):
        """
        Obtener todos los almacenes
        ---
        tags:
          - Almacenes
        responses:
          200:
            description: Lista de almacenes obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_repository:
                    type: integer
                  name:
                    type: string
                  location:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
          400:
            description: Error interno
        """
        try:
            repositories = repository_service.get_all()
            repositories_list = [repository.to_json() for repository in repositories]
            return repositories_list, 200
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def post(self):
        """
        Crear un nuevo almacén
        ---
        tags:
          - Almacenes
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
                location:
                  type: string
                  example: "string"
              required:
                - name
                - location
        responses:
          200:
            description: Almacén creado exitosamente
            schema:
              type: object
              properties:
                id_repository:
                  type: integer
                name:
                  type: string
                location:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          400:
            description: El nombre del almacén ya existe o error de validación
        """
        try:
            data = request.get_json()
            validated_data = RepositorySchema.model_validate(data)

            repository = repository_service.get_by_name(validated_data.name)

            if repository:
                return {
                    'error': "repository name already exists"
                }, 400

            create_repository = repository_service.create(validated_data)

            return create_repository.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerRepositoryResource(Resource):

    @jwt_required()
    def get(self, id_repository: int):
        """
        Obtener un almacén por ID
        ---
        tags:
          - Almacenes
        parameters:
          - in: path
            name: id_repository
            type: integer
            required: true
            description: ID del almacén
        responses:
          200:
            description: Almacén encontrado
            schema:
              type: object
              properties:
                id_repository:
                  type: integer
                name:
                  type: string
                location:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          404:
            description: Almacén no encontrado
        """
        try:
            repository = repository_service.get_by_id(id_repository)

            if repository is None:
                return {
                    'error': "repository not found"
                }, 404

            return repository.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_repository: int):
        """
        Actualizar un almacén por ID
        ---
        tags:
          - Almacenes
        parameters:
          - in: path
            name: id_repository
            type: integer
            required: true
            description: ID del almacén
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "string"
                location:
                  type: string
                  example: "string"
              required:
                - name
                - location
        responses:
          200:
            description: Almacén actualizado exitosamente
          400:
            description: El nombre del almacén ya existe o error de validación
          404:
            description: Almacén no encontrado
        """
        try:
            repository = repository_service.get_by_id(id_repository)

            if repository is None:
                return {
                    'error': "repository not found"
                }, 404

            data = request.get_json()
            validated_data = RepositorySchema.model_validate(data)

            repository = repository_service.get_by_name(validated_data.name)
            if repository :
                return {
                    'error': "repository name already exists"
                }, 400

            update_repository = repository_service.update(repository, validated_data)

            return update_repository.to_json(), 200

        except ValidationError as e:
            return {
                'error': str(e.errors())
            }, 400
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_repository: int):
        """
        Eliminar un almacén por ID
        ---
        tags:
          - Almacenes
        parameters:
          - in: path
            name: id_repository
            type: integer
            required: true
            description: ID del almacén
        responses:
          200:
            description: Almacén eliminado exitosamente
          404:
            description: Almacén no encontrado
        """
        try:
            repository = repository_service.get_by_id(id_repository)

            if repository is None:
                return {
                    'error': "repository not found"
                }, 404

            repository_service.delete(repository)

            return None, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400
