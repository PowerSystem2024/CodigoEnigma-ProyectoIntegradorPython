from sqlalchemy.orm import Session
from app.modules.patentes.models.patente_model import Patente
from typing import Optional, List

class PatenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Patente]:
        return self.db.query(Patente).filter_by(activo=True).all()

    def get_all_incluyendo_inactivas(self):
        return self.db.query(Patente).all()

    def get_by_patente(self, patente: str) -> Optional[Patente]:
        return self.db.query(Patente).filter(Patente.patente == patente).first()

    def add(self, patente: Patente) -> Patente:
        self.db.add(patente)
        self.db.commit()
        self.db.refresh(patente)
        return patente

    def delete(self, patente: str) -> Optional[Patente]:
        obj = self.get_by_patente(patente)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def update_patente(self, patente_original: str, patente_nueva: str) -> Optional[Patente]:
        obj = self.get_by_patente(patente_original)
        if obj:
            obj.patente = patente_nueva
            self.db.commit()
            self.db.refresh(obj)
        return obj
