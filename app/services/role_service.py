from db import db
from app.models.role_model import Role
from app.schemas.role_schema import RoleSchema

class RoleService:

    def get_all(self) -> list[Role]:
        roles = Role.query.filter_by(status=True).all()
        return roles
    
    def get_by_name(self, name: str) -> Role | None:
        name = Role.query.filter_by(name=name).first()
        return name
    
    def get_by_id(self, id_role: int) -> Role | None:

        role = Role.query.filter_by(id_role=id_role).first()
        return role
    
    def create(self, data: RoleSchema) -> Role:

        role = Role(
            name=data.name,
            description=data.description
        )

        db.session.add(role)
        db.session.commit()

        return role

    def update(self, role: Role, data: RoleSchema) -> Role:
        
        role.name = data.name
        role.description = data.description
        db.session.commit()
        
        return role
    
    def delete(self, role: Role) -> Role:

        role.status = False
        db.session.commit()
        
        return role
    

role_service = RoleService()