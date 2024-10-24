from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    ## TODO: Remove localhost when deploying to prod.
    CORS(app, supports_credentials=True, origins=['*'])
    app.config['SECRET_KEY'] = os.getenv('FLASK_SESSION_SECRET_KEY')

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8) ## Will be lower when we implment refresh tokens
    # NOTE: X-CSRF-TOKEN Header is not needed on GET requests You get this from the csrf_access_token cookie in the login response this is javascript enabled cookie
    jwt = JWTManager(app)

    from api.orders.orders_controller import orders
    app.register_blueprint(orders, url_prefix='/orders/')



    return app
