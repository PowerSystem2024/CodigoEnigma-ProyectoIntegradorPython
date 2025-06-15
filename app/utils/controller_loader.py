import os
import importlib
from typing import Optional


def import_controllers(base_path: Optional[str] = "app/modules") -> None:
    """
    Dynamically imports all controller modules from the specified base path.

    This function ensures that all controllers inside the `controllers/` folder
    of each module are loaded before registering them in the API. This is
    necessary because Flask-RESTx requires namespaces to be defined before
    they can be registered.

    Args:
        base_path (Optional[str]): The base directory where modules are located.
                                   Defaults to "app/modules".

    Behavior:
        - Iterates through subdirectories in `base_path` (each representing a module).
        - If a module has a `controllers/` folder, it imports all `.py` files inside.
        - Skips `__init__.py` to avoid redundant imports.
        - Logs a warning if a module has no controllers.

    Example:
        Given the structure:
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

        The function will:
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
