from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.models.company_model import Company
from app.schemas.company_schema import CompanySchema
from app.services.company_service import company_service

class CompanyResource(Resource):
    
    @jwt_required()
    def get(self):
        """
        Obtener todas las empresas
        ---
        tags:
          - Empresas
        responses:
          200:
            description: Lista de empresas obtenida exitosamente
            schema:
              type: array
              items:
                type: object
                properties:
                  id_company:
                    type: integer
                  name:
                    type: string
                  ruc:
                    type: string
                  address:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
          400:
            description: Error interno
        """
        try:

            companies: list[Company] = company_service.get_all()
            companies_list = [company.to_json() for company in companies]
            return companies_list, 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def post(self):
        """
        Crear una nueva empresa
        ---
        tags:
          - Empresas
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
                ruc:
                  type: string
                  example: "string"
                address:
                  type: string
                  example: "string"
              required:
                - name
                - ruc
                - address
        responses:
          200:
            description: Empresa creada exitosamente
            schema:
              type: object
              properties:
                id_company:
                  type: integer
                name:
                  type: string
                ruc:
                  type: string
                address:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          400:
            description: La empresa ya existe o error de validación
        """
        try:
            data = request.get_json()
            validated_data = CompanySchema.model_validate(data)

            company = company_service.get_by_name(validated_data.name)

            if company:
                return {
                    'error': 'company name already exists'
                }, 400
            
            create_company = company_service.create(validated_data)

            return create_company.to_json(), 200
            
        except ValidationError as e:
            return {
                'error': str(e.errors())
            }
        except Exception as e:
            return {
                'error': str(e)
            }, 400

class ManagerCompanyResource(Resource):
    
    @jwt_required()
    def get(self, id_company: int):
        """
        Obtener una empresa por ID
        ---
        tags:
          - Empresas
        parameters:
          - in: path
            name: id_company
            type: integer
            required: true
            description: ID de la empresa
        responses:
          200:
            description: Empresa encontrada
            schema:
              type: object
              properties:
                id_company:
                  type: integer
                name:
                  type: string
                ruc:
                  type: string
                address:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
          404:
            description: Empresa no encontrada
        """
        try:
            
            company = company_service.get_by_id(id_company)

            if company is None:
                return {
                    'error': 'company not found'
                }, 404
            
            return company.to_json(), 200

        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def put(self, id_company):
        """
        Actualizar una empresa por ID
        ---
        tags:
          - Empresas
        parameters:
          - in: path
            name: id_company
            type: integer
            required: true
            description: ID de la empresa
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "string"
                ruc:
                  type: string
                  example: "string"
                address:
                  type: string
                  example: "string"
              required:
                - name
                - ruc
                - address
        responses:
          200:
            description: Empresa actualizada exitosamente
          400:
            description: Error de validación
          404:
            description: Empresa no encontrada
        """
        try:
            company = company_service.get_by_id(id_company)

            if company is None:
                return {
                    'error': 'company not found'
                }, 404
            
            data = request.get_json()
            validated_data = CompanySchema.model_validate(data)

            company_update = company_service.update(company, validated_data)

            return company_update.to_json(), 200
            
        except ValidationError as e:
            return {
                'error': str(e.errors())
            }
        except Exception as e:
            return {
                'error': str(e)
            }, 400

    @jwt_required()
    def delete(self, id_company):
        """
        Eliminar una empresa por ID
        ---
        tags:
          - Empresas
        parameters:
          - in: path
            name: id_company
            type: integer
            required: true
            description: ID de la empresa
        responses:
          200:
            description: Empresa eliminada exitosamente
          404:
            description: Empresa no encontrada
        """
        try:
            company = company_service.get_by_id(id_company)

            if company is None:
                return {
                    'error': 'company not found'
                }, 404
            
            company_service.delete(company)

            return None, 200
            
        except Exception as e:
            return {
                'error': str(e)
            }, 400