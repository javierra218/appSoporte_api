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

    def update_trabajador(self, id_trabajador: int, trabajador: TrabajadorBase):
        existing_trabajador = self.get_trabajador(id_trabajador)
        if existing_trabajador:
            existing_trabajador.nombre_trabajador = trabajador.nombre_trabajador
            existing_trabajador.peso_acumulado = trabajador.peso_acumulado
            self.db.commit()
            self.db.refresh(existing_trabajador)
        return existing_trabajador

    # def update_trabajador(self, id_trabajador: int, trabajador: TrabajadorBase):
    #     existing_trabajador = self.get_trabajador(id_trabajador)
    #     if existing_trabajador:
    #         for key, value in trabajador.model_dump().items():
    #             setattr(existing_trabajador, key, value)
    #         self.db.commit()
    #         self.db.refresh(existing_trabajador)
    #     return existing_trabajador

    def delete_trabajador(self, id_trabajador: int):
        trabajador = self.get_trabajador(id_trabajador)
        if trabajador:
            self.db.delete(trabajador)
            self.db.commit()
            return True
        return False

    def get_trabajador_detalles(self, id_trabajador: int):
        trabajador = self.get_trabajador(id_trabajador)
        if trabajador:
            asignaciones = (
                self.db.query(Asignacion)
                .filter(Asignacion.id_trabajador == id_trabajador)
                .all()
            )
            detalles = {"trabajador": trabajador, "soportes_asignados": asignaciones}
            return detalles
        return None

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

    def update_soporte(self, id_soporte: int, soporte: SoporteBase):
        existing_soporte = self.get_soporte(id_soporte)
        if existing_soporte:
            existing_soporte.nombre_soporte = soporte.nombre_soporte
            existing_soporte.descripcion = soporte.descripcion
            existing_soporte.prioridad = soporte.prioridad
            existing_soporte.peso_trabajo = soporte.peso_trabajo
            self.db.commit()
            self.db.refresh(existing_soporte)
        return existing_soporte

    # def update_soporte(self, id_soporte: int, soporte: SoporteBase):
    #     existing_soporte = self.get_soporte(id_soporte)
    #     if existing_soporte:
    #         for key, value in soporte.model_dump().items():
    #             setattr(existing_soporte, key, value)
    #         self.db.commit()
    #         self.db.refresh(existing_soporte)
    #     return existing_soporte

    def delete_soporte(self, id_soporte: int):
        soporte = self.get_soporte(id_soporte)
        if soporte:
            self.db.delete(soporte)
            self.db.commit()
            return True
        return False

    def get_soporte_detalles(self, id_soporte: int):
        soporte = self.get_soporte(id_soporte)
        if soporte:
            asignacion = (
                self.db.query(Asignacion)
                .filter(Asignacion.id_soporte == id_soporte)
                .first()
            )
            detalles = {"soporte": soporte, "trabajador_asignado": asignacion}
            return detalles
        return None


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
        trabajadores = (
            self.db.query(Trabajador).order_by(Trabajador.peso_acumulado).all()
        )
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
