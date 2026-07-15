from flask_restful import Resource
from flask import request, jsonify, make_response,session
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required,logout_user,current_user
from controllers.database import db
from controllers.models import Student,Company,Application,Drive
from datetime import date,datetime


class CompanyDashboardAPI(Resource):

    @auth_token_required
    @roles_required("Company")
    def get(self):

        company = Company.query.filter_by(user_id = current_user.id).first()
        if not company:
            result = {
                "message": "Company profile not found"
            }

            return make_response(jsonify(result),400)
        
        active_drives = Drive.query.filter(
            Drive.company_id == company.id,
            Drive.status == "Approved",
            Drive.deadline_date >= date.today()
        ).count()

        total_drives = Drive.query.filter_by(company_id=company.id).count()

        total_applicants = (
            Application.query.join(Drive, Application.drive_id == Drive.id)
            .filter(Drive.company_id == company.id).count()
        )


        response = {
            "message": "Company dashboard fetched successfully",
            "company": {
                "id": company.id,
                "name": company.name,
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "hr_contact": company.hr_contact,
                "website": company.website,
                "status": company.status
            },
            "statistics": {
                "active_drives": active_drives,
                "total_drives": total_drives,
                "total_applicants": total_applicants
            },
            "can_create_drive": company.status == "Approved" 
        }
        return make_response(jsonify(response),200)
    

class CompanyProfileAPI(Resource):

    @auth_token_required
    @roles_required("Company")
    def put(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        if not company:
            result = {
                "message": "Company profile not found"
            }
            return make_response(jsonify(result),404)
        
        profile_cred = request.get_json()

        if not profile_cred:
            result = {
                "message": "Profile data is required"
            }
            return make_response(jsonify(result),400)
        
        name = profile_cred.get("name")
        hr_name = profile_cred.get("hr_name")
        hr_email = profile_cred.get("hr_email")
        hr_contact = profile_cred.get("hr_contact")
        website = profile_cred.get("website")

        if not all([name,hr_contact,hr_email,hr_name,website]):
            result = {
                "message": "Please fill all required fields"
            }
            return make_response(jsonify(result),400)
        
        existing = Company.query.filter_by(hr_email=hr_email).first()
        if existing and existing.id != company.id: 
            result = {
                "message": "This email is already registered with another company"
            } 
            return make_response(jsonify(result), 409)
        
        company.name = name
        company.hr_name = hr_name
        company.hr_email = hr_email
        company.hr_contact = hr_contact
        company.website = website

        db.session.commit()

        response = {
            "message": "Company profile updated successfully",
            "company": {
                "id": company.id,
                "name": company.name,
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "hr_contact": company.hr_contact,
                "website": company.website,
                "status": company.status
            }
        }

        return  make_response(jsonify(response),200)
    
class CompanyDriveAPI(Resource):

    @auth_token_required
    @roles_required("Company")
    def post(self):
        company = Company.query.filter_by(user_id=current_user.id).first()

        if not company:
            result = {
                "message": "Company profile not found"
            }
            return make_response(jsonify(result),404)
        
        if company.status != "Approved":
            result = {
                "message": "Admin approval is required to create a drive"
            }
            return make_response(jsonify(result),403)
        
        drive_cred = request.get_json()

        if not drive_cred:
            result = {
                "message": "Drive details are required"
            }
            return make_response(jsonify(result),400)
        
        title = drive_cred.get("title")
        description = drive_cred.get("description")
        branches = drive_cred.get("branches")
        year = drive_cred.get("year")
        deadline = drive_cred.get("deadline_date")

        if not title or not description or not branches or year is None or not deadline:
            result = {
                "message": "Please fill all the required fields"
            }
            return make_response(jsonify(result),400)
        
        if not isinstance(branches, list):
            result = {
                "message": "Branches must be provided as a list"
            }
            return make_response(jsonify(result),400)
        
        try:
            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            result = {
                "message": "Deadline must use YYYY-MM-DD format"
            }
            return make_response(jsonify(result),400)
        
        drive = Drive(
            title=title,
            description=description,
            branches=",".join(branches),
            year = int(year),
            deadline_date= deadline_date,
            status = "Pending",
            company_id = company.id
        )

        db.session.add(drive)
        db.session.commit()

        result = {
            "message": "Drive submitted for admin approval",
            "drive": {
                "id": drive.id,
                "title": drive.title,
                "description": drive.description,
                "branches": drive.branches.split(","),
                "year": drive.year,
                "deadline_date": drive.deadline_date.isoformat(),
                "status": drive.status
            }
        }

        return make_response(jsonify(result),201)
    
    @auth_token_required
    @roles_required("Company")
    def get(self):
        company  = Company.query.filter_by(
            user_id = current_user.id
        ).first()

        if not company:
            result = {
                "message": "Company profile not found"
            }
            return make_response(jsonify(result),404)
        
        drives = Drive.query.filter_by(
            company_id=company.id
        ).order_by(Drive.id.desc()).all()

        drive_list = []

        for drive in drives:
            applicant_count = Application.query.filter_by(
                drive_id=drive.id
            ).count()

            is_active = (
                drive.status == "Approved"
                and drive.deadline_date >= date.today()
            )

            drive_list.append({
                "id": drive.id,
                "title": drive.title,
                "description": drive.description,
                "branches": drive.branches.split(","),
                "year": drive.year,
                "deadline_date": drive.deadline_date.isoformat(),
                "status": drive.status,
                "is_active": is_active,
                "applicant_count": applicant_count
        })
            
        result = {
            "message": "Company drives fetched successfully",
            "total_drives": len(drive_list),
            "drive": drive_list
        }
        return make_response(jsonify(result),200)

class DriveApplicationAPI(Resource):

    @auth_token_required
    @roles_required("Company")
    def get(self,drive_id):
        company = Company.query.filter_by(user_id=current_user.id).first()

        if not company:
            result = {
                "message": "Company profile not found"
            }
            return make_response(jsonify(result),404)
        
        drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first()

        if not drive:
            result = {
                "message": "Drive not found or access denied"
            }
            return make_response(jsonify(result),404)
        
        applications = Application.query.filter_by(
            drive_id=drive.id
        ).order_by(Application.applied_date.desc()).all()

        applicants = []

        for application in applications:
            student = db.session.get(Student, application.student_id)

            if student:
                applicants.append({
                    "application_id": application.id,
                    "student_id": student.id,
                    "name": student.name,
                    "email": student.user.email,
                    "branch": student.branch,
                    "year": student.year,
                    "applied_date": application.applied_date.isoformat(),
                    "status": application.status
                })


        result = {
            "message": "Applicants fetched successfully",
                "drive": {
                    "id": drive.id,
                    "title": drive.title,
                    "status": drive.status
                },
                "total_applicants": len(applicants),
                "applicants": applicants
        }
        return make_response(jsonify(result), 200)

class ApplicationStatusAPI(Resource):

    @auth_token_required
    @roles_required("Company")
    def patch(self, application_id):
        company = Company.query.filter_by(
            user_id=current_user.id
        ).first()

        if not company:
            return {
                "message": "Company profile not found"
            }, 404

        application = (
            Application.query
            .join(Drive, Application.drive_id == Drive.id)
            .filter(
                Application.id == application_id,
                Drive.company_id == company.id
            )
            .first()
        )

        if not application:
            return {
                "message": "Application not found or access denied"
            }, 404

        data = request.get_json()

        if not data or not data.get("status"):
            return {
                "message": "Application status is required"
            }, 400

        new_status = data.get("status")

        allowed_statuses = [
            "Applied",
            "Shortlisted",
            "Selected",
            "Rejected"
        ]

        if new_status not in allowed_statuses:
            return {
                "message": "Invalid application status",
                "allowed_statuses": allowed_statuses
            }, 400

        application.status = new_status
        db.session.commit()

        return {
            "message": "Application status updated successfully",
            "application": {
                "id": application.id,
                "drive_id": application.drive_id,
                "student_id": application.student_id,
                "status": application.status
            }
        }, 200