from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.router import create_routers
from flask_restx import Api
from app.db.database import init_db
from flask import render_template
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "front_end", "templates"),
        static_folder=os.path.join(BASE_DIR, "front_end", "static"),
    )

    init_db()

    # Enable CORS for all routes and origins
    CORS(app)

    # Disable masks for optional fields in Swagger
    app.config["RESTX_MASK_SWAGGER"] = False

    api = Api(
        app,
        version="1.0",
        title="Sistema de Gestión de Patentes",
        description="API para gestionar patentes de vehículos.",
        doc="/docs",
        openapi="3.0.0",
    )

    # Register namespaces after defining the routes
    create_routers(api)

    # Configure Swagger UI
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(api.__schema__)
    
    # Registro front
    @app.route("/home")
    def index():
        return render_template("index.html")

    
    return app


app = create_app()
