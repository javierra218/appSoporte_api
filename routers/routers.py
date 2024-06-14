from typing import List, Optional
from fastapi import APIRouter, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from models.models import Trabajador, Soporte
from services.services import TrabajadorService, SoporteService, AsignacionService
from schemas.schemas import TrabajadorBase, SoporteBase, AsignacionBase

soporte_router = APIRouter()


# Endpoints de Trabajador
@soporte_router.post(
    "/trabajadores", tags=["Trabajadores"], response_model=TrabajadorBase
)
def create_trabajador(trabajador: TrabajadorBase):
    db = SessionLocal()
    result = TrabajadorService(db).create_trabajador(trabajador)
    if result:
        return JSONResponse(
            status_code=201, content={"message": "Trabajador creado exitosamente"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al crear el trabajador"}
    )


@soporte_router.get(
    "/trabajadores", tags=["Trabajadores"], response_model=List[TrabajadorBase]
)
def get_trabajadores():
    db = SessionLocal()
    result = TrabajadorService(db).get_trabajadores()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@soporte_router.post("/trabajadores/reset", tags=["Trabajadores"], response_model=dict)
def reset_pesos_acumulados():
    db = SessionLocal()
    result = TrabajadorService(db).reset_pesos_acumulados()
    if result:
        return JSONResponse(
            status_code=200, content={"message": "Pesos acumulados reseteados"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al resetear los pesos acumulados"}
    )


@soporte_router.put(
    "/trabajadores/{id_trabajador}",
    tags=["Trabajadores"],
    response_model=TrabajadorBase,
)
def update_trabajador(id_trabajador: int, trabajador: TrabajadorBase):
    db = SessionLocal()
    existing_trabajador = TrabajadorService(db).get_trabajador(id_trabajador)
    if not existing_trabajador:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    updated_trabajador = TrabajadorService(db).update_trabajador(
        id_trabajador, trabajador
    )
    return JSONResponse(status_code=200, content=jsonable_encoder(updated_trabajador))


@soporte_router.delete(
    "/trabajadores/{id_trabajador}", tags=["Trabajadores"], response_model=dict
)
def delete_trabajador(id_trabajador: int):
    db = SessionLocal()
    result = TrabajadorService(db).delete_trabajador(id_trabajador)
    if result:
        return JSONResponse(
            status_code=200, content={"message": "Trabajador eliminado exitosamente"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al eliminar el trabajador"}
    )


@soporte_router.get(
    "/trabajadores/{id_trabajador}/detalles", tags=["Trabajadores"], response_model=dict
)
def get_trabajador_detalles(id_trabajador: int):
    db = SessionLocal()
    trabajador = TrabajadorService(db).get_trabajador_detalles(id_trabajador)
    if not trabajador:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return JSONResponse(status_code=200, content=jsonable_encoder(trabajador))


# Endpoints de Soporte
@soporte_router.post("/soportes", tags=["Soportes"], response_model=SoporteBase)
def create_soporte(soporte: SoporteBase):
    db = SessionLocal()
    result = SoporteService(db).create_soporte(soporte)
    if result:
        return JSONResponse(
            status_code=201, content={"message": "Soporte creado exitosamente"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al crear el soporte"}
    )


@soporte_router.get("/soportes", tags=["Soportes"], response_model=List[SoporteBase])
def get_soportes():
    db = SessionLocal()
    result = SoporteService(db).get_soportes()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@soporte_router.put(
    "/soportes/{id_soporte}", tags=["Soportes"], response_model=SoporteBase
)
def update_soporte(id_soporte: int, soporte: SoporteBase):
    db = SessionLocal()
    existing_soporte = SoporteService(db).get_soporte(id_soporte)
    if not existing_soporte:
        raise HTTPException(status_code=404, detail="Soporte no encontrado")
    updated_soporte = SoporteService(db).update_soporte(id_soporte, soporte)
    return JSONResponse(status_code=200, content=jsonable_encoder(updated_soporte))


@soporte_router.delete("/soportes/{id_soporte}", tags=["Soportes"], response_model=dict)
def delete_soporte(id_soporte: int):
    db = SessionLocal()
    result = SoporteService(db).delete_soporte(id_soporte)
    if result:
        return JSONResponse(
            status_code=200, content={"message": "Soporte eliminado exitosamente"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al eliminar el soporte"}
    )


@soporte_router.get(
    "/soportes/{id_soporte}/detalles", tags=["Soportes"], response_model=dict
)
def get_soporte_detalles(id_soporte: int):
    db = SessionLocal()
    soporte = SoporteService(db).get_soporte_detalles(id_soporte)
    if not soporte:
        raise HTTPException(status_code=404, detail="Soporte no encontrado")
    return JSONResponse(status_code=200, content=jsonable_encoder(soporte))


# Endpoints de Asignación
@soporte_router.post(
    "/asignaciones", tags=["Asignaciones"], response_model=AsignacionBase
)
def create_asignacion(asignacion: AsignacionBase):
    db = SessionLocal()
    result = AsignacionService(db).create_asignacion(asignacion)
    if result:
        return JSONResponse(
            status_code=201, content={"message": "Asignación creada exitosamente"}
        )
    return JSONResponse(
        status_code=400, content={"message": "Error al crear la asignación"}
    )


@soporte_router.get(
    "/asignaciones", tags=["Asignaciones"], response_model=List[AsignacionBase]
)
def get_asignaciones():
    db = SessionLocal()
    result = AsignacionService(db).get_asignaciones()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@soporte_router.post("/asignaciones/assign", tags=["Asignaciones"], response_model=dict)
def assign_support(soporte: SoporteBase):
    db = SessionLocal()
    result = AsignacionService(db).assign_support(soporte)
    if result:
        trabajador_asignado = (
            db.query(Trabajador)
            .filter(Trabajador.id_trabajador == result.id_trabajador)
            .first()
        )
        response_content = {
            "message": "Soporte asignado exitosamente",
            "trabajador": {
                "id_trabajador": trabajador_asignado.id_trabajador,
                "nombre_trabajador": trabajador_asignado.nombre_trabajador,
                "peso_acumulado": trabajador_asignado.peso_acumulado,
            },
        }
        return JSONResponse(status_code=201, content=response_content)
    return JSONResponse(
        status_code=400, content={"message": "Error al asignar el soporte"}
    )
