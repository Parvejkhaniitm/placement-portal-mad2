from flask_restful import Resource
from flask import request, jsonify, make_response,session
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required,logout_user
from controllers.database import db
from controllers.models import Student,Company,Drive


class PendingComapnayAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self):

        companies = Company.query.filter_by(status="Pending").all()

        result = []
        for company in companies:
            result.append({
                "id": company.id,
                "name": company.name,
                "hr_email": company.hr_email,
                "website": company.website,
                "status": company.status
            })

        return make_response(jsonify(result),200)
    
class ApproveCompanyAPI(Resource):
    
    @auth_token_required
    @roles_required("admin")
    def put(self, company_id):

        company = Company.query.get(company_id)
        if not company:
            result = {
                "message": "Company not found"
            }

            return make_response(jsonify(result),400)

        company.status = "Approved"
        db.session.commit()
        result = {
            "message": "Comapny approved successfully"
        }

        return make_response(jsonify(result),200)

class RejectCompanyAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self, company_id):

        company = Company.query.get(company_id)

        if not company:
            result = {
                "message": "Company not found"
            }
            return make_response(jsonify(result),400)
        
        company.status = "Rejected"

        db.session.commit()
        result = {
            "message": "Company Rejected successfully"
        }
        return make_response(jsonify(result),200)

class StatsAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self):

        total_students = Student.query.count()
        total_company = Company.query.count()
        total_drive = Drive.query.count()  
        total_pending_company = Company.query.filter_by(status="Pending").count()

        response = {
            "total_students": total_students,
            "total_company": total_company,
            "total_drive": total_drive,
            "total_pending_company": total_pending_company
        }

        return make_response(jsonify(response),200)
    
class StudentListAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self):

        student_list = Student.query.all()

        result = []

        for student in student_list:
            result.append({
                "id": student.id,
                "name": student.name,
                "branch": student.branch,
                "status": student.status,
                "year": student.year
            })
        return make_response(jsonify(result),200)
    
    
class BlacklistStudentAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self,student_id):

        student = Student.query.get(student_id)
        if not student:
            result = {
                "message": "Student not found"
            }
            return make_response(jsonify(result),400)
        
        student.status = "Blacklisted"
        db.session.commit()

        result = {
            "message": "Student Blacklisted successfully"
        }
        return make_response(jsonify(result),200)
    
class ReactivateStudentAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self,student_id):

        student = Student.query.get(student_id)

        if not student:
            result ={
                "message": "Student not found"
            }
            return make_response(jsonify(result),400)
        
        student.status = "Active"
        db.session.commit()

        result  = {
            "message": "Student activated successfully"
        }
        
        return make_response(jsonify(result),200)



class BlacklistCompanyAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self, company_id):

        company = Company.query.get(company_id)
        if not company:
            result = {
                "message": " Company not found"
            }
            return make_response(jsonify(result),400)
        
        company.status = "Blacklisted"
        db.session.commit()

        result = {
            "message": "Company blacklisted Successfully"
        }
        return make_response(jsonify(result),200)
    
class CompanylistAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):

        companies = Company.query.all()
        
        result = []
        for company in companies:
            result.append(
                {
                    "id": company.id,
                    "name": company.name,
                    "hr_email": company.hr_email,
                    "hr_contact": company.hr_contact,
                    "website": company.website,
                    "status": company.status
                }
            )
        return make_response(jsonify(result),200)