from db import db
from app.models.category_model import Category
from app.schemas.category_schema import CategorySchema

class CategoryService:
    
    def get_all(self) -> list[Category]:
        categories = Category.query.filter_by(status=True).all()
        return categories
    
    def get_by_name(self, name: str) -> Category | None:
        category = Category.query.filter_by(name=name).first()
        return category
    
    def get_by_id(self, id_category: int) -> Category | None:
        category = Category.query.filter_by(id_category=id_category).first()
        return category

    def create(self, data: CategorySchema) -> Category:

        create_category = Category(
            name = data.name,
            description= data.description
        )

        db.session.add(create_category)
        db.session.commit()

        return create_category

    def update(self, category: Category, data: CategorySchema) -> Category:

        category.name = data.name
        category.description = data.description
        db.session.commit()

        return category
    
    def delete(self, category: Category) -> Category:

        category.status = False
        db.session.commit()
        return category

category_service = CategoryService()
    
