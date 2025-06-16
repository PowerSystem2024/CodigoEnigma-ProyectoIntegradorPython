import os
import importlib
from flask_restx import Api


def register_namespace(api: Api, base_path: str = "app/modules") -> None:
    """
    Automatically imports and registers all namespaces from the modules into the provided API instance.

    The function dynamically scans the `base_path` directory for subdirectories (modules). Each module is expected
    to contain an `__init__.py` file and define a namespace variable (`ns_<module_name>`). The module's name
    (i.e., the folder name) is used as the URL prefix for the corresponding namespace in the API.

    Args:
        api (Api): The Flask-RESTx API instance where the namespaces will be registered.
        base_path (str): The base directory where the modules are located. Defaults to `"app/modules"`.

    Behavior:
        - Iterates through all subdirectories in `base_path`.
        - If a subdirectory contains an `__init__.py` file, it is considered a module and imported dynamically.
        - The function looks for a namespace variable (`ns_<module_name>`) inside the module.
        - If the namespace is found, it is registered in the API with a route prefix matching the module name.
        - If the namespace is not found, a warning is printed.
        - If a subdirectory does not contain an `__init__.py`, it is ignored.

    Example:
        Assuming the following module structure:
        ```
        app/modules/
        ├── users/
        │   ├── __init__.py  # Defines `ns_users`
        │   ├── controller.py
        ├── products/
        │   ├── __init__.py  # Defines `ns_products`
        │   ├── controller.py
        ```

        The function will:
        - Import `app.modules.users` and `app.modules.products`.
        - Look for `ns_users` inside `app.modules.users` and register it under `/users`.
        - Look for `ns_products` inside `app.modules.products` and register it under `/products`.

    """
    for module in os.listdir(base_path):
        module_path = os.path.join(base_path, module, "__init__.py")
        if os.path.exists(module_path):
            # Import the module dynamically
            module_name = f"app.modules.{module}"
            importlib.import_module(module_name)

            # Retrieve the namespace object (e.g., ns_module) from the module
            ns = getattr(importlib.import_module(module_name), f"ns_{module}", None)
            if ns:
                # Register the namespace with the API
                api.add_namespace(ns, path=f"/{module}")
            else:
                # Log a warning if the namespace is not found
                print(f"Namespace '{module}' not found in {module_name}.")
        else:
            # Log a warning if the module does not exist
            print(f"Module '{module}' does not exist in {base_path}.")
