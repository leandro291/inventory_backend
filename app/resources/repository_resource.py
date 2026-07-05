from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.schemas.repository_schema import RepositorySchema
from app.services.repository_service import repository_service

class RepositoryResource(Resource):

    @jwt_required()
    def get(self):
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
