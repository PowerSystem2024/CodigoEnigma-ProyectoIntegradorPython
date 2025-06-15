from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


DATABASE_URL = "sqlite:///./app/patentes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseTableBuilder:
    """
    A class that facilitates the creation of tables in a database using SQLAlchemy.

    Attributes:
        - Base: An SQLAlchemy base object used to define the structure of tables.
        - engine: A database engine connection object used for executing operations on the database.

    Methods:
        - create_table: A method that uses the Base object to create all tables defined in SQLAlchemy in the database
        associated with the engine.
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
    Initializes the database by creating all tables defined in the models.
    """
    from app.modules.patentes.models import patente_model  # importa todos los modelos aquí

    engine = DatabaseTableBuilder.get_engine()
    Base = DatabaseTableBuilder.get_base()
    Base.metadata.create_all(engine)
