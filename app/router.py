from flask_restful import Api

from app import app
from app.resources.auth_resource import LoginResource, RegisterResource
from app.resources.role_resource import RoleResource, ManagerRoleResource
from app.resources.company_resource import CompanyResource, ManagerCompanyResource
from app.resources.supplier_resource import SupplierResource, ManagerSupplierResource
from app.resources.category_resource import CategoryResource, ManagerCategoryResource
from app.resources.repository_resource import RepositoryResource, ManagerRepositoryResource
from app.resources.type_movement_resource import TypeMovementResource, ManagerTypeMovementResource
from app.resources.product_resource import ProductResource, ManagerProductResource
from app.resources.inventory_resource import InventoryResource, ManagerInventoryResource
from app.resources.movement_resource import MovementResource, ManagerMovementResource

api = Api(app, prefix="/api/v1")

api.add_resource(LoginResource, "/auth/login")
api.add_resource(RegisterResource, "/auth/register")

api.add_resource(CategoryResource, "/category")
api.add_resource(ManagerCategoryResource, "/category/<int:id_category>")

api.add_resource(RoleResource, "/role")
api.add_resource(ManagerRoleResource, "/role/<int:id_role>")

api.add_resource(SupplierResource, "/supplier")
api.add_resource(ManagerSupplierResource, "/supplier/<int:id_supplier>")

api.add_resource(RepositoryResource, "/repository")
api.add_resource(ManagerRepositoryResource, "/repository/<int:id_repository>")

api.add_resource(TypeMovementResource, "/type-movement")
api.add_resource(ManagerTypeMovementResource, "/type-movement/<int:id_type_movement>")

api.add_resource(ProductResource, "/product")
api.add_resource(ManagerProductResource, "/product/<int:id_product>")

api.add_resource(CompanyResource, "/company")
api.add_resource(ManagerCompanyResource, "/company/<int:id_company>")

api.add_resource(InventoryResource, "/inventory")
api.add_resource(ManagerInventoryResource, "/inventory/<int:id_inventory>")

api.add_resource(MovementResource, "/movement")
api.add_resource(ManagerMovementResource, "/movement/<int:id_movement>")