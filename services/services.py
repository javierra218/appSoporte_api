from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.models import Trabajador, Soporte, Asignacion
from schemas.schemas import TrabajadorBase, SoporteBase, AsignacionBase
import random


class TrabajadorService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_trabajador(self, trabajador: TrabajadorBase):
        new_trabajador = Trabajador(**trabajador.model_dump())
        self.db.add(new_trabajador)
        self.db.commit()
        self.db.refresh(new_trabajador)
        return new_trabajador

    def get_trabajadores(self):
        return self.db.query(Trabajador).all()

    def get_trabajador(self, id_trabajador: int):
        return (
            self.db.query(Trabajador)
            .filter(Trabajador.id_trabajador == id_trabajador)
            .first()
        )
    
    def reset_pesos_acumulados(self):
        trabajadores = self.get_trabajadores()
        for trabajador in trabajadores:
            trabajador.peso_acumulado = 0
        self.db.commit()
        return trabajadores


class SoporteService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_soporte(self, soporte: SoporteBase):
        new_soporte = Soporte(**soporte.model_dump())
        self.db.add(new_soporte)
        self.db.commit()
        self.db.refresh(new_soporte)
        return new_soporte

    def get_soportes(self):
        return self.db.query(Soporte).all()

    def get_soporte(self, id_soporte: int):
        return self.db.query(Soporte).filter(Soporte.id_soporte == id_soporte).first()


class AsignacionService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_asignacion(self, asignacion: AsignacionBase):
        new_asignacion = Asignacion(**asignacion.model_dump())
        self.db.add(new_asignacion)
        self.db.commit()
        self.db.refresh(new_asignacion)
        return new_asignacion

    def get_asignaciones(self):
        return self.db.query(Asignacion).all()

    def get_asignacion(self, id_asignacion: int):
        return (
            self.db.query(Asignacion)
            .filter(Asignacion.id_asignacion == id_asignacion)
            .first()
        )

    def buscar_trabajador_con_menos_carga(self):
        trabajadores = self.db.query(Trabajador).order_by(Trabajador.peso_acumulado).all()
        if not trabajadores:
            return None

        min_peso = trabajadores[0].peso_acumulado
        candidatos = [t for t in trabajadores if t.peso_acumulado == min_peso]
        return random.choice(candidatos)

    def assign_support(self, soporte: SoporteBase):
        trabajador = self.buscar_trabajador_con_menos_carga()
        if not trabajador:
            return None

        new_soporte = Soporte(**soporte.model_dump())
        self.db.add(new_soporte)
        self.db.commit()
        self.db.refresh(new_soporte)

        new_asignacion = Asignacion(
            id_trabajador=trabajador.id_trabajador,
            id_soporte=new_soporte.id_soporte,
            fecha_asignacion=datetime.now(timezone.utc),
        )
        self.db.add(new_asignacion)
        trabajador.peso_acumulado += new_soporte.peso_trabajo
        self.db.commit()
        return new_asignacion
