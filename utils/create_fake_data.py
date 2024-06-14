import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from sqlalchemy.orm import Session
from config.database import engine, Base, SessionLocal
from models.models import Trabajador, Soporte, Asignacion
from services.services import AsignacionService, TrabajadorService, SoporteService
from schemas.schemas import TrabajadorBase, SoporteBase
import random

fake = Faker()

def create_fake_data():
    db = SessionLocal()
    
    # Crear trabajadores
    trabajadores_data = [
        {"nombre_trabajador": "Pedro", "peso_acumulado": 0},
        {"nombre_trabajador": "Felipe", "peso_acumulado": 0},
        {"nombre_trabajador": "Andrea", "peso_acumulado": 0}
    ]
    
    trabajadores = [Trabajador(**data) for data in trabajadores_data]
    db.bulk_save_objects(trabajadores)
    db.commit()

    # Verificar la creación de trabajadores
    trabajadores_creados = db.query(Trabajador).all()
    print(f"Trabajadores creados: {len(trabajadores_creados)}")

    # Crear soportes ficticios
    prioridades = [1, 2, 3, 4, 5]
    pesos_trabajo = [1, 2, 3, 4, 5]
    for _ in range(20):
        soporte = Soporte(
            nombre_soporte=fake.word(),
            descripcion=fake.text(max_nb_chars=200),
            prioridad=random.choice(prioridades),
            peso_trabajo=random.choice(pesos_trabajo)
        )
        db.add(soporte)
    db.commit()

    # Verificar la creación de soportes
    soportes_creados = db.query(Soporte).all()
    print(f"Soportes creados: {len(soportes_creados)}")

    # Asignar soportes automáticamente
    asignacion_service = AsignacionService(db)
    for soporte in soportes_creados:
        asignacion_service.assign_support(SoporteBase(
            nombre_soporte=soporte.nombre_soporte,
            descripcion=soporte.descripcion,
            prioridad=soporte.prioridad,
            peso_trabajo=soporte.peso_trabajo
        ))

    db.commit()

    # Verificar las asignaciones
    asignaciones_creadas = db.query(Asignacion).all()
    print(f"Asignaciones creadas: {len(asignaciones_creadas)}")

    # Mostrar el peso acumulado de cada trabajador
    for trabajador in trabajadores_creados:
        print(f"Trabajador: {trabajador.nombre_trabajador}, Peso Acumulado: {trabajador.peso_acumulado}")

    db.close()

if __name__ == "__main__":
    create_fake_data()
    print("Datos ficticios creados y verificados exitosamente.")
