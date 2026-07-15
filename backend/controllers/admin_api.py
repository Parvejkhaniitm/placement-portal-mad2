from flask_restful import Resource
from flask import request, jsonify, make_response,session
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required,logout_user
from controllers.database import db
from controllers.models import Student,Company,Drive,Application
from cache import get_cache, set_cache, delete_cache


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
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "hr_contact": company.hr_contact,
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

        delete_cache("admin_dashboard_stats")
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
        delete_cache("admin_dashboard_stats")
        result = {
            "message": "Company Rejected successfully"
        }
        return make_response(jsonify(result),200)

class StatsAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self):

        cache_key = "admin_dashboard_stats"

        cached_stats = get_cache(cache_key)

        if cached_stats:
            return make_response(jsonify(cached_stats), 200)

        total_students = Student.query.count()
        total_company = Company.query.count()
        total_drive = Drive.query.count()
        total_pending_company = Company.query.filter_by(
            status="Pending"
        ).count()

        response = {
            "total_students": total_students,
            "total_company": total_company,
            "total_drive": total_drive,
            "total_pending_company": total_pending_company
        }

        set_cache(cache_key, response, timeout=60)

        return make_response(jsonify(response), 200)
    
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
                "email": student.user.email,
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
        delete_cache("admin_dashboard_stats")

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
        delete_cache("admin_dashboard_stats")

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
        delete_cache("admin_dashboard_stats")

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
                    "hr_name": company.hr_name,
                    "hr_email": company.hr_email,
                    "hr_contact": company.hr_contact,
                    "website": company.website,
                    "status": company.status
                }
            )
        return make_response(jsonify(result),200)


class PendingDriveAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self):

        drives = Drive.query.filter_by(
            status="Pending"
        ).all()

        result = []

        for drive in drives:
            result.append({
                "id": drive.id,
                "title": drive.title,
                "company_name": drive.company.name,
                "branches": drive.branches.split(","),
                "year": drive.year,
                "deadline_date":
                    drive.deadline_date.isoformat(),
                "status": drive.status,
                "description": drive.description,
            })

        return make_response(jsonify(result), 200)


class ApproveDriveAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self, drive_id):

        drive = db.session.get(Drive, drive_id)

        if not drive:
            return {
                "message": "Drive not found"
            }, 404

        drive.status = "Approved"
        db.session.commit()
        delete_cache("admin_dashboard_stats")

        return {
            "message": "Drive approved successfully"
        }, 200


class RejectDriveAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self, drive_id):

        drive = db.session.get(Drive, drive_id)

        if not drive:
            return {
                "message": "Drive not found"
            }, 404

        drive.status = "Rejected"
        db.session.commit()
        delete_cache("admin_dashboard_stats")

        return {
            "message": "Drive rejected successfully"
        }, 200

class CompanyDriveHistoryAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self, company_id):

        company = db.session.get(Company, company_id)

        if not company:
            return {
                "message": "Company not found"
            }, 404

        drives = Drive.query.filter_by(
            company_id=company.id
        ).order_by(Drive.id.desc()).all()

        result = []

        for drive in drives:
            applicant_count = Application.query.filter_by(
                drive_id=drive.id
            ).count()

            result.append({
                "id": drive.id,
                "title": drive.title,
                "description": drive.description,
                "branches": drive.branches.split(","),
                "year": drive.year,
                "deadline_date": drive.deadline_date.isoformat(),
                "status": drive.status,
                "applicant_count": applicant_count
            })

        return make_response(jsonify({
            "company": {
                "id": company.id,
                "name": company.name
            },
            "drives": result
        }), 200)



