from app.utils.controller_loader import import_controllers
from app.utils.register_namespace import register_namespace
# from flask import render_template
from flask_restx import Api


def create_routers(api: Api) -> None:
    """
    Registra los espacios de nombres en la instancia de API proporcionada.

    Args:
        api (Api): La instancia de API de Flask-RESTx donde se registrarán los espacios de nombres.
    """
    # Paso 1: Importar todos los controladores para asegurarse de que estén cargados antes del registro en la API de Flask-RESTx
    import_controllers()

    # Paso 2: Registrar todos los espacios de nombres para asociarlos con la API
    register_namespace(api)