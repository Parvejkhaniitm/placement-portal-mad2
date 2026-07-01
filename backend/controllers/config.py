class Config:

    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "password"
    SECURITY_PASSWORD_HASH = "bcrypt"