from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import (
    auth_token_required,
    roles_required,
    current_user
)

from controllers.database import db
from controllers.models import Student, Drive, Application
from datetime import date


class StudentDashboardAPI(Resource):

    @auth_token_required
    @roles_required("Student")
    def get(self):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if not student:
            response = {
                "message": "Student profile not found"
            }

            return make_response(jsonify(response), 404)

        total_applications = Application.query.filter_by(
            student_id=student.id
        ).count()

        selected_applications = Application.query.filter_by(
            student_id=student.id,
            status="Selected"
        ).count()

        active_drives = Drive.query.filter(
            Drive.status == "Approved",
            Drive.deadline_date >= date.today()
        ).count()

        response = {
            "message": "Student dashboard fetched successfully",

            "student": {
                "id": student.id,
                "name": student.name,
                "email": student.user.email,
                "branch": student.branch,
                "year": student.year,
                "status": student.status
            },

            "statistics": {
                "active_drives": active_drives,
                "total_applications": total_applications,
                "selected_applications": selected_applications
            },

            "can_apply": student.status == "Active"
        }

        return make_response(jsonify(response), 200)
    

class StudentProfileAPI(Resource):

    @auth_token_required
    @roles_required("Student")
    def put(self):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if not student:
            response = {
                "message": "Student profile not found"
            }

            return make_response(jsonify(response), 404)

        profile_data = request.get_json()

        if not profile_data:
            response = {
                "message": "Profile data is required"
            }

            return make_response(jsonify(response), 400)

        name = profile_data.get("name")
        branch = profile_data.get("branch")
        year = profile_data.get("year")

        if not name or not branch or not year:
            response = {
                "message": "Please fill all required fields"
            }

            return make_response(jsonify(response), 400)

        allowed_branches = [
            "CSE",
            "IT",
            "ECE",
            "Mechanical"
        ]

        if branch not in allowed_branches:
            response = {
                "message": "Invalid branch selected"
            }

            return make_response(jsonify(response), 400)

        try:
            year = int(year)
        except ValueError:
            response = {
                "message": "Year must be a number"
            }

            return make_response(jsonify(response), 400)

        if year not in [1, 2, 3, 4]:
            response = {
                "message": "Invalid year selected"
            }

            return make_response(jsonify(response), 400)

        student.name = name
        student.branch = branch
        student.year = year

        db.session.commit()

        response = {
            "message": "Profile updated successfully",

            "student": {
                "id": student.id,
                "name": student.name,
                "email": student.user.email,
                "branch": student.branch,
                "year": student.year,
                "status": student.status
            }
        }

        return make_response(jsonify(response), 200)
    



class StudentDriveListAPI(Resource):

    @auth_token_required
    @roles_required("Student")
    def get(self):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if not student:
            response = {
                "message": "Student profile not found"
            }

            return make_response(jsonify(response), 404)

        drives = Drive.query.filter(
            Drive.status == "Approved",
            Drive.deadline_date >= date.today()
        ).order_by(Drive.deadline_date.asc()).all()

        result = []

        for drive in drives:

            already_applied = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first() is not None

            eligible_branches = [
                branch.strip()
                for branch in drive.branches.split(",")
            ]

            branch_allowed = student.branch in eligible_branches

            year_allowed = year_allowed = drive.year == 0 or student.year == drive.year

            result.append({
                "id": drive.id,
                "title": drive.title,
                "description": drive.description,
                "company_name": drive.company.name,
                "branches": drive.branches.split(","),
                "year": drive.year,
                "deadline_date": drive.deadline_date.isoformat(),
                "status": drive.status,
                "already_applied": already_applied,
                "is_eligible": branch_allowed and year_allowed
            })

        return make_response(jsonify(result), 200)
    

class ApplyDriveAPI(Resource):

    @auth_token_required
    @roles_required("Student")
    def post(self, drive_id):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if not student:
            response = {
                "message": "Student profile not found"
            }

            return make_response(jsonify(response), 404)

        if student.status != "Active":
            response = {
                "message": "Your account is not active. You cannot apply."
            }

            return make_response(jsonify(response), 403)

        drive = db.session.get(Drive, drive_id)

        if not drive:
            response = {
                "message": "Drive not found"
            }

            return make_response(jsonify(response), 404)

        if drive.status != "Approved":
            response = {
                "message": "This drive is not open for applications"
            }

            return make_response(jsonify(response), 403)

        if drive.deadline_date < date.today():
            response = {
                "message": "Application deadline has passed"
            }

            return make_response(jsonify(response), 403)


        eligible_branches = [
            branch.strip()
            for branch in drive.branches.split(",")
        ]

        
        branch_allowed = student.branch in eligible_branches
        year_allowed = drive.year == 0 or student.year == drive.year

        if not branch_allowed or not year_allowed:
            response = {
                "message": "You are not eligible for this drive"
            }

            return make_response(jsonify(response), 403)

        existing_application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

        if existing_application:
            response = {
                "message": "You have already applied for this drive"
            }

            return make_response(jsonify(response), 409)

        application = Application(
            student_id=student.id,
            drive_id=drive.id,
            status="Applied"
        )

        db.session.add(application)
        db.session.commit()

        response = {
            "message": "Application submitted successfully",

            "application": {
                "id": application.id,
                "student_id": application.student_id,
                "drive_id": application.drive_id,
                "status": application.status,
                "applied_date": application.applied_date.isoformat()
            }
        }

        return make_response(jsonify(response), 201)
    

class StudentApplicationListAPI(Resource):

    @auth_token_required
    @roles_required("Student")
    def get(self):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if not student:
            response = {
                "message": "Student profile not found"
            }

            return make_response(jsonify(response), 404)

        applications = Application.query.filter_by(
            student_id=student.id
        ).order_by(Application.applied_date.desc()).all()

        result = []

        for application in applications:
            drive = db.session.get(Drive, application.drive_id)

            if drive:
                result.append({
                    "application_id": application.id,
                    "drive_id": drive.id,
                    "drive_title": drive.title,
                    "company_name": drive.company.name,
                    "applied_date": application.applied_date.isoformat(),
                    "deadline_date": drive.deadline_date.isoformat(),
                    "status": application.status
                })

        return make_response(jsonify(result), 200)
    
