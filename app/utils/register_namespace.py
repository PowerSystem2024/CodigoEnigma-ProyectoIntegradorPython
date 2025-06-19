import os
import importlib
from flask_restx import Api


def register_namespace(api: Api, base_path: str = "app/modules") -> None:
    """
    Importa y registra automáticamente todos los espacios de nombres desde los módulos en la instancia de API proporcionada.

    La función escanea dinámicamente el directorio `base_path` en busca de subdirectorios (módulos). Se espera que cada módulo
    contenga un archivo `__init__.py` y defina una variable de espacio de nombres (`ns_<module_name>`). El nombre del módulo
    (es decir, el nombre de la carpeta) se utiliza como prefijo de URL para el espacio de nombres correspondiente en la API.

    Args:
        api (Api): La instancia de API de Flask-RESTx donde se registrarán los espacios de nombres.
        base_path (str): El directorio base donde se encuentran los módulos. Predeterminado es `"app/modules"`.

    Comportamiento:
        - Itera a través de todos los subdirectorios en `base_path`.
        - Si un subdirectorio contiene un archivo `__init__.py`, se considera un módulo y se importa dinámicamente.
        - La función busca una variable de espacio de nombres (`ns_<module_name>`) dentro del módulo.
        - Si se encuentra el espacio de nombres, se registra en la API con un prefijo de ruta que coincide con el nombre del módulo.
        - Si no se encuentra el espacio de nombres, se imprime una advertencia.
        - Si un subdirectorio no contiene un `__init__.py`, se ignora.

    Ejemplo:
        Dada la siguiente estructura de módulos:
        ```
        app/modules/
        ├── users/
        │   ├── __init__.py  # Defines `ns_users`
        │   ├── controller.py
        ├── products/
        │   ├── __init__.py  # Defines `ns_products`
        │   ├── controller.py
        ```

        La función realizará lo siguiente:
        - Import `app.modules.users` and `app.modules.products`.
        - Look for `ns_users` inside `app.modules.users` and register it under `/users`.
        - Look for `ns_products` inside `app.modules.products` and register it under `/products`.

    """
    for module in os.listdir(base_path):
        module_path = os.path.join(base_path, module, "__init__.py")
        if os.path.exists(module_path):
            # Importar el módulo dinámicamente
            module_name = f"app.modules.{module}"
            importlib.import_module(module_name)

            # Recuperar el objeto de espacio de nombres (por ejemplo, ns_module) del módulo
            ns = getattr(importlib.import_module(module_name), f"ns_{module}", None)
            if ns:
                # Registrar el espacio de nombres en la API
                api.add_namespace(ns, path=f"/{module}")
            else:
                # Registrar una advertencia si no se encuentra el espacio de nombres
                print(f"Namespace '{module}' not found in {module_name}.")
        else:
            # Registrar una advertencia si el módulo no existe
            print(f"Module '{module}' does not exist in {base_path}.")
