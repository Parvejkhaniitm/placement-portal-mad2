from flask_restful import Resource
from flask import request, jsonify, make_response,session
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required,logout_user
from controllers.database import db
from controllers.models import Student,Company



class LoginAPI(Resource):
    def post(self):

        login_cred = request.get_json()

        if not login_cred:
            result = {
                'message': 'Login Credentials are required'
            }
            return make_response(jsonify(result), 400)
        
        email = login_cred.get('email')
        password = login_cred.get('password')

        if not email or not password:
            result = {
                'message': 'Email and Password are required'
            }
            return make_response(jsonify(result), 400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            result = {
                "message": "User not found. Please register"
            }
            return make_response(jsonify(result),404)
        
        if not utils.verify_password(password, user.password):
            result = {
                'message': 'Invalid Password'
            }
            return make_response(jsonify(result),401)
        
        auth_token = user.get_auth_token()
        
        utils.login_user(user)

        response = {
            "message": "Login successful.",
            'user_details' : {
                'Email' : user.email,
                'Roles' : [role.name for role in user.roles],
                'auth_token': auth_token,
            }
        }

        return make_response(jsonify(response), 200)

class LogoutAPI(Resource):

    @auth_token_required # this check wether user is already Login or not 
    # @roles_required(['admin'])
    def post(self):
        logout_user()

        response = {
            'message': 'Logout successful'
        }
    
        return make_response(jsonify(response),200)
    
class StudentRegisterAPI(Resource):

    
    def post(self):
        register_cred = request.get_json()
        
        if not register_cred:
            result = {
                'message': 'Register credentials are required'
            }
            return make_response(jsonify(result))
        
        name = register_cred.get("name")
        email = register_cred.get("email")
        branch = register_cred.get("branch")
        year = register_cred.get("year")
        password = register_cred.get("password")
        confirm_password = register_cred.get("confirm_password")

        if not all([name,email,branch,year,password,confirm_password]):
            result = {
                'message' : 'Please fill all the require fields'
            }
            return make_response(jsonify(result))
        
        if password != confirm_password:
            result = {
                "message": "Passwords do not match"
            }
            return make_response(jsonify(result))
        
        existing_user = user_datastore.find_user(email=email)

        if existing_user:
            result = {
                'message' : 'Email already register. Please login'
            }
            return make_response(jsonify(result))
        
        student_role = user_datastore.find_role("Student")

        user = user_datastore.create_user(
            email = email,
            password = utils.hash_password(password),
            roles = [student_role]
        )

        db.session.flush()

        student = Student(
            name = name,
            branch = branch,
            year = year,
            user_id = user.id
        )
        db.session.add(student)
        db.session.commit()

        response = {
            'message': 'Registration successful'
        }
        return make_response(jsonify(response),200)

class CompanyRegisterAPI(Resource):

    def post(self):

        register_cred = request.get_json()
        if not register_cred:
            result = {
                "message": "Register credentials are required"
            }
            return make_response(jsonify(result))
        
        name = register_cred.get("name")
        hr_name = register_cred.get("hr_name")
        hr_email = register_cred.get("hr_email")
        phone = register_cred.get("phone")
        website = register_cred.get("website")
        password = register_cred.get("password")
        confirm_password = register_cred.get("confirm_password") 

        if not all([name,hr_name,hr_email,phone,website,password,confirm_password]):
            result = {
                "message": "Please fill all the require fields"
            }
            return make_response(jsonify(result))
        
        if password != confirm_password:
            result = {
                "message": "Passwords do not match"
            }
            return make_response(jsonify(result))
        
        existing_user = user_datastore.find_user(email=hr_email)
        if existing_user:
            result = {
                "message" : "Email already register. Please login"
            }
            return make_response(jsonify(result), 409)
        
        company_role = user_datastore.find_role("Company")
        user = user_datastore.create_user(
            email = hr_email,
            password = utils.hash_password(password),
            roles = [company_role]
        )
        db.session.flush()

        company = Company(
            name = name,
            hr_name = hr_name,
            hr_email = hr_email,
            hr_contact = phone,
            website = website,
            user_id = user.id
        )
        db.session.add(company)
        db.session.commit()

        response = {
            "message" : "Registration successful"
        }
        return make_response(jsonify(response),200)



        





    
        




        
