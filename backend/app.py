from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore,hash_password
from controllers.config import Config
from controllers.user_datastore import user_datastore
from flask_restful import Api
from controllers.database import db

from flask_cors import CORS



def create_app(): 
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore) #

    api = Api(app,prefix='/api')
    

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin',description="Administrator")
        student_role = user_datastore.find_or_create_role(name='Student',description="Student")
        company_role = user_datastore.find_or_create_role(name='Company',description='Company')

        if not user_datastore.find_user(email="admin@gmail.com"):
            user_datastore.create_user(
                email="admin@gmail.com",
                password = hash_password("admin123"),
                roles = [admin_role] # here the role is relatioship that is why we used list
                )
            db.session.commit()
        




    return app,api

app,api = create_app()
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5173"])

from controllers.authentication_apis import LoginAPI,LogoutAPI,StudentRegisterAPI,CompanyRegisterAPI
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI,'/logout')
api.add_resource(StudentRegisterAPI,'/student_register')
api.add_resource(CompanyRegisterAPI,'/company_register')

from controllers.admin_api import PendingComapnayAPI,ApproveCompanyAPI,RejectCompanyAPI,StatsAPI,StudentListAPI,BlacklistStudentAPI,ReactivateStudentAPI,BlacklistCompanyAPI,CompanylistAPI
api.add_resource(PendingComapnayAPI, '/admin/pending-company')
api.add_resource(ApproveCompanyAPI, '/admin/company/<int:company_id>/approve')
api.add_resource(RejectCompanyAPI, '/admin/company/<int:company_id>/reject')
api.add_resource(StatsAPI, '/admin/stats')
api.add_resource(StudentListAPI, '/admin/students')
api.add_resource(BlacklistStudentAPI, '/admin/student/<int:student_id>/blacklist')
api.add_resource(ReactivateStudentAPI, '/admin/student/<int:student_id>/reactivate')
api.add_resource(BlacklistCompanyAPI, '/admin/company/<int:company_id>/blacklist')
api.add_resource(CompanylistAPI, '/admin/company-list')

from controllers.company_api import CompanyDashboardAPI,CompanyProfileAPI,CompanyDriveAPI, DriveApplicationAPI, ApplicationStatusAPI
api.add_resource(CompanyDashboardAPI, '/company/dashboard')
api.add_resource(CompanyProfileAPI, '/company/profile')
api.add_resource(CompanyDriveAPI, '/company/drive')
api.add_resource(DriveApplicationAPI, '/company/drive/<int:drive_id>/applicants')
api.add_resource(ApplicationStatusAPI, '/company/application/<int:application_id>/status')






if __name__ == "__main__":
    app.run(debug=True)

