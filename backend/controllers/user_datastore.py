from flask_security import Security, SQLAlchemyUserDatastore
from controllers.models import User, Role

from controllers.database import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
