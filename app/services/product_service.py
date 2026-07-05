from app.models.product_model import Product
from app.schemas.product_schema import ProductSchema
from db import db

class ProductService:

    def get_all(self) -> list[Product]:
        products = Product.query.filter_by(status=True).all()
        return products
    
    def get_by_id(self, id_product: int) -> Product | None:
        product = Product.query.filter_by(id_product=id_product).first()
        return product
    
    def get_last(self) -> Product | None:
        product = Product.query.order_by(
            Product.id_product.desc()
        ).first()
        return product

    def create(self, data: ProductSchema, code: str, image: str) -> Product:
        product = Product(
            name=data.name,
            code=code,
            description=data.description,
            image=image,
            brand=data.brand,
            purchase_price=data.purchase_price,
            sale_price=data.sale_price,
            id_category=data.id_category
        )

        db.session.add(product)
        db.session.commit()

        return product
    
    def update(self, data: ProductSchema, product: Product, image: str | None) -> Product:

        if image:
            product.image = image

        product.name = data.name
        product.description = data.description
        product.brand = data.brand
        product.purchase_price = data.purchase_price
        product.sale_price = data.sale_price
        product.id_category = data.id_category

        db.session.commit()

        return product
    
    def delete(self, product: Product) -> None:

        product.status = False

        db.session.commit()

product_service = ProductService()