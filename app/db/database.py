from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


DATABASE_URL = "sqlite:///./app/patentes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseTableBuilder:
    """
    Una clase que facilita la creación de tablas en una base de datos utilizando SQLAlchemy.

    Atributos:
        - Base: Un objeto base de SQLAlchemy utilizado para definir la estructura de las tablas.
        - engine: Un objeto de conexión de motor de base de datos utilizado para ejecutar operaciones en la base de datos.

    Métodos:
        - create_table: Un método que utiliza el objeto Base para crear todas las tablas definidas en SQLAlchemy en la base de datos asociada con el motor.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._base = declarative_base()
            cls._instance._engine = engine
        return cls._instance

    @staticmethod
    def get_base():
        if DatabaseTableBuilder._instance is None:
            DatabaseTableBuilder._instance = DatabaseTableBuilder()
        return DatabaseTableBuilder._instance._base

    @staticmethod
    def get_engine():
        if DatabaseTableBuilder._instance is None:
            DatabaseTableBuilder._instance = DatabaseTableBuilder()
        return DatabaseTableBuilder._instance._engine

    def create_table(self):
        try:
            self._base.metadata.create_all(self._engine, checkfirst=True)
        except OperationalError as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    """
    from app.modules.patentes.models import patente_model  # importa todos los modelos aquí

    engine = DatabaseTableBuilder.get_engine()
    Base = DatabaseTableBuilder.get_base()
    Base.metadata.create_all(engine)
