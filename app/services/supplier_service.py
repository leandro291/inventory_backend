from db import db
from app.models.supplier_model import Supplier
from app.schemas.supplier_schema import SupplierSchema

class SupplierService:

    def get_all(self) -> list[Supplier]:
        suppliers = Supplier.query.filter_by(is_active=True).all()
        return suppliers
    
    def get_by_email(self, email: str) -> Supplier | None:
        supplier = Supplier.query.filter_by(email=email).first()
        return supplier
    
    def get_by_id(self, id_supplier: int) -> Supplier | None:
        supplier = Supplier.query.filter_by(id_supplier=id_supplier).first()
        return supplier
    
    def create(self, data: SupplierSchema) -> Supplier:

        create_supplier = Supplier(
            name=data.name,
            email=data.email,
            telephone=data.telephone,
            id_company=data.id_company
        )

        db.session.add(create_supplier)
        db.session.commit()

        return create_supplier

    def update(self, supplier: Supplier, data: SupplierSchema) -> Supplier:

        supplier.name = data.name
        supplier.email = data.email
        supplier.telephone = data.telephone
        supplier.id_company = data.id_company

        db.session.commit()

        return supplier

    def delete(self, supplier: Supplier) -> Supplier:

        supplier.is_active = False
        db.session.commit()

        return supplier

supplier_service = SupplierService()