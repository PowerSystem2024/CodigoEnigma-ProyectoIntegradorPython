from app.utils.controller_loader import import_controllers
from app.utils.register_namespace import register_namespace
# from flask import render_template
from flask_restx import Api


def create_routers(api: Api) -> None:
    """
    Registers namespaces in the provided API instance.

    Args:
        api (Api): The Flask-RESTx API instance where namespaces will be registered.
    """
    # Step 1: Import all controllers to ensure they are loaded before registration for the Flask-RESTx API
    import_controllers()

    # Step 2: Register all namespaces to associate them with the API
    register_namespace(api)

    # @app.route("/")
    # def index():
    #     return render_template("index.html")