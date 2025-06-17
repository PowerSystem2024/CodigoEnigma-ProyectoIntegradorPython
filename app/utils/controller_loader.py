import os
import importlib
from typing import Optional


def import_controllers(base_path: Optional[str] = "app/modules") -> None:
    """
    Importa dinámicamente todos los módulos de controladores desde la ruta base especificada.

    Esta función garantiza que todos los controladores dentro de la carpeta `controllers/` de cada módulo se carguen antes de registrarlos en la API. 
    Esto es necesario porque Flask-RESTx requiere que los espacios de nombres se definan antes de que puedan registrarse.

    Args:
        base_path (Optional[str]): El directorio base donde se encuentran los módulos.
                                   Predeterminado es "app/modules".

    Comportamiento:
        - Itera a través de los subdirectorios en `base_path` (cada uno representando un módulo).
        - Si un módulo tiene una carpeta `controllers/`, importa todos los archivos `.py` dentro.
        - Omite `__init__.py` para evitar importaciones redundantes.
        - Registra una advertencia si un módulo no tiene controladores.

    Ejemplo:
        Dada la estructura:
        ```
        app/modules/
        ├── users/
        │   ├── controllers/
        │   │   ├── __init__.py
        │   │   ├── user_controller.py
        ├── products/
        │   ├── controllers/
        │   │   ├── product_controller.py
        ```

        La función hará lo siguiente:
        - Import `app.modules.users.controllers.user_controller`
        - Import `app.modules.products.controllers.product_controller`
    """
    for module in os.listdir(base_path):
        module_path = os.path.join(base_path, module, "controllers")
        if os.path.exists(module_path):
            # Iterate through all Python files in the controllers folder
            for filename in os.listdir(module_path):
                if filename.endswith(".py") and filename != "__init__.py":
                    # Dynamically import each controller module
                    module_name = f"app.modules.{module}.controllers.{filename[:-3]}"
                    importlib.import_module(module_name)
