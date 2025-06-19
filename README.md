# Estacionamiento

## Descripción
Este proyecto es una aplicación web diseñada para gestionar el cobro de estacionamiento según el tiempo de permanencia del vehículo. Permite registrar el ingreso y egreso de vehículos, calcular automáticamente el monto a pagar en función del tiempo transcurrido, y brindar una experiencia rápida y eficiente tanto para operadores como para usuarios.

## Estructura del proyecto

El proyecto sigue una organización modular para mejorar la mantenibilidad y escalabilidad.

```
CodigoEnigma-ProyectoIntegradorPython/
├── app/
│   ├── front_end/            # Frontend de la aplicación
│   ├── db/                   # Gestión de la conexión a la base de datos
│   ├── modules/              # Organización modular de la aplicación
│   │   ├── patentes/         # Módulo de gestión de patente
│   │   │   ├── controllers/  # Controladores que gestionan las solicitudes HTTP
│   │   │   │   └── utils/    # Utilidades para los controladores
│   │   │   ├── models/       # Definición del esquema de las patentes
│   │   │   ├── repositories/ # Acceso a la base de datos o API externas
│   │   │   └── services/     # Lógica de negocio
│   ├── utils/                # Utilidades generales del proyecto
│   │   ├── controller_loader.py  # Carga dinámica de controladores
│   │   └── register_namespace.py # Registro dinámico de namespaces de la API
│   ├── __init__.py           # Inicializa la aplicación Flask
│   ├── router/
│   │   └── __init__.py       # Configuración y registro de rutas de la API
└── run.py                    # Punto de entrada principal para ejecutar la aplicación
```

## Instalación

### Requisitos previos

- Python 3.x

### Instalación local

1. **Clonar el repositorio**

  Cloná el repositorio desde GitHub:

   ```
   git clone https://github.com/PowerSystem2024/CodigoEnigma-ProyectoIntegradorPython.git
   cd CodigoEnigma-ProyectoIntegradorPython
   ```

2. **Crear un entorno virtual**

   Creá un entorno virtual con el siguiente comando:

   ```
   python -m venv env
   ```

3. **Activar el entorno virtual**

   - En Windows:

     ```
     python -m venv venv.\venv\Scripts\activate
     ```

   - En macOS/Linux:

     ```
     source env/bin/activate
     ```

4. **Instalar dependencias**

   Una vez dentro del entorno virtual, instalá las dependencias necesarias con pip:

   ```
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación**

   Podés ejecutar la aplicación con el siguiente comando:

   ```
   python run.py
   ```

   La API estará disponible en `http://127.0.0.1:5000/home`. 


## Swagger UI

La documentación de la API está disponible a través de Swagger UI. Podés acceder a ella en:

```
http://localhost:5000/docs
```

Ahí podés ver todos los endpoints de la API y probarlos directamente desde el navegador.

![alt text](image.png)

---

# CodigoEnigma-ProyectoIntegradorPython

Version 1.0

1. Se toma como punto de partida, la funcionalidad de CRUD de forma web.
2. De momento solo se asegura la funcionalidad, luego se avanzará con el almacenamiento de BDD.
3. Tambien se avanzará en el avance de diseño.

Version 1.1

1. Se corrigen detalles de tipografía y organización de la carpeta y su versión.
2. Se realizó de forma exitosa la conexión con la base de datos.
3. Se utilizó la libreria TinyDB para asegurar la compatibilidad con el proyecto.
4. Se avanza con la siguiente versión

Version 1.2

1. Se aseguró la funcionalidad de los botones.
2. Se agregó botón "Verificar servidor" que indica en tiempo real si el servidor se encuentra en funcionamiento o no.
3. Se agregó timer.

Version 1.3

1. Se trabajó en el diseño
2. Se agregaron estilos para mejorar la estructura responsive