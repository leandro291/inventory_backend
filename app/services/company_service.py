from db import db
from app.models.company_model import Company
from app.schemas.company_schema import CompanySchema

class CompanyService:
    
    def get_all(self) -> list[Company]:
        companies = Company.query.filter_by(status=True).all()
        return companies
    
    def get_by_name(self, name: str) -> Company | None:
        company = Company.query.filter_by(name=name).first()
        return company

    def get_by_id(self, id_company: int) -> Company | None:
        company = Company.query.filter_by(id_company=id_company).first()
        return company

    def create(self, data: CompanySchema) -> Company:

        create_company = Company(
            name= data.name,
            ruc= data.ruc,
            address=data.address
        )

        db.session.add(create_company)
        db.session.commit()

        return create_company
    
    def update(self, company: Company, data: CompanySchema) -> Company:

        company.name = data.name
        company.ruc = data.ruc
        company.address = data.address

        db.session.commit()

        return company
    
    def delete(self, company: Company) -> Company:

        company.status = False
        db.session.commit()
        return company

company_service = CompanyService()