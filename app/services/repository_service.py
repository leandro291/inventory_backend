from app.models.repository_model import Repository
from app.schemas.repository_schema import RepositorySchema
from db import db

class RepositoryService:

    def get_all(self) -> list[Repository]:
        repositories = Repository.query.filter_by(is_active=True).all()
        return repositories

    def get_by_name(self, name: str) -> Repository | None:
        repository = Repository.query.filter_by(name=name).first()
        return repository

    def get_by_id(self, id_repository: int) -> Repository | None:
        repository = Repository.query.filter_by(id_repository=id_repository).first()
        return repository

    def create(self, data: RepositorySchema) -> Repository:

        create_repository = Repository(
            name=data.name,
            location=data.location
        )

        db.session.add(create_repository)
        db.session.commit()

        return create_repository

    def update(self, repository: Repository, data: RepositorySchema) -> Repository:

        repository.name = data.name
        repository.location = data.location

        db.session.commit()

        return repository

    def delete(self, repository: Repository) -> Repository:

        repository.is_active = False
        db.session.commit()

        return repository

repository_service = RepositoryService()
