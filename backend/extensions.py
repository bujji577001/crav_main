from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Create the extension instances here
db = SQLAlchemy()
security = Security()
api = Api()
jwt = JWTManager()
migrate = Migrate()
