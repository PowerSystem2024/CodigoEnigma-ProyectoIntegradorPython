from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.db.database import DatabaseTableBuilder
from datetime import datetime

Base = DatabaseTableBuilder.get_base()

class Patente(Base):
    __tablename__ = "patentes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patente = Column(String, nullable=False, unique=True)
    hora_ingreso = Column(String, nullable=False)
    precio_hora = Column(Float, nullable=False)
    hora_actualizacion = Column(DateTime, nullable=False)
    activo = Column(Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patente': self.patente,
            'hora_ingreso': self.hora_ingreso,
            'precio_hora': self.precio_hora,
            'hora_actualizacion': self.hora_actualizacion.isoformat() if self.hora_actualizacion else None,
            'activo': self.activo
        }
