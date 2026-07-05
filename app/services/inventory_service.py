from db import db
from app.models.inventory_model import Inventory
from app.schemas.inventory_schema import InventorySchema

class InventoryService:

    def get_all(self) -> list[Inventory]:
        inventories = Inventory.query.filter_by(is_active=True).all()
        return inventories

    def get_by_id(self, id_inventory: int) -> Inventory | None:
        inventory = Inventory.query.filter_by(id_inventory=id_inventory).first()
        return inventory

    def get_by_product_and_repository(self, id_product: int, id_repository: int) -> Inventory | None:
        inventory = Inventory.query.filter_by(
            id_product=id_product,
            id_repository=id_repository,
        ).first()
        return inventory

    def create(self, data: InventorySchema) -> Inventory:
        inventory = Inventory(
            stock=data.stock,
            id_product=data.id_product,
            id_repository=data.id_repository,
        )
        db.session.add(inventory)
        db.session.commit()
        return inventory

    def update(self, inventory: Inventory, data: InventorySchema) -> Inventory:
        inventory.stock = data.stock
        db.session.commit()
        return inventory

    def delete(self, inventory: Inventory) -> Inventory:
        inventory.is_active = False
        db.session.commit()
        return inventory


inventory_service = InventoryService()
