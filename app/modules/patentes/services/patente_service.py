from sqlalchemy.orm import Session
from app.modules.patentes.models.patente_model import Patente
from app.modules.patentes.repositories.patente_repository import PatenteRepository
from typing import Optional, List
from datetime import datetime

class PatenteService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PatenteRepository(db)

    def listar(self) -> List[Patente]:
        return self.repository.get_all()

    def listar_todas(self):
        return self.repository.get_all_incluyendo_inactivas()

    def agregar(self, data: dict) -> Patente:
        if self.repository.get_by_patente(data["patente"]):
            raise ValueError("La patente ya existe.")
        patente = Patente(**data)
        
        hora_ingreso_str = data.get('hora_ingreso')
        hora_actualizacion_str = data.get('hora_actualizacion')
        hora_ingreso = hora_ingreso_str  # Si tu modelo espera string, déjalo así
        hora_actualizacion = datetime.fromisoformat(hora_actualizacion_str)
        
        patente = Patente(
            patente=data['patente'],
            hora_ingreso=hora_ingreso,
            precio_hora=data['precio_hora'],
            hora_actualizacion=hora_actualizacion
        )
        
        return self.repository.add(patente)

    def eliminar(self, patente: str) -> Patente:
        obj = self.repository.delete(patente)
        if not obj:
            raise ValueError("Patente no encontrada.")
        return obj

    def actualizar(self, patente_original: str, patente_nueva: str, precio_hora: Optional[float] = None, hora_actualizacion_str: Optional[str] = None) -> Patente:
        obj = self.repository.get_by_patente(patente_original)
        if not obj:
            raise ValueError("Registro no encontrado.")
        if hora_actualizacion_str:
            hora_actualizacion = datetime.fromisoformat(hora_actualizacion_str)
            obj.hora_actualizacion = hora_actualizacion
        obj.patente = patente_nueva
        if precio_hora is not None:
            obj.precio_hora = precio_hora
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def marcar_inactiva(self, patente: str) -> bool:
        obj = self.repository.get_by_patente(patente)
        if obj:
            obj.activo = False
            self.db.commit()
            return True
        return False
