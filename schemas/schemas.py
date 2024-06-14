from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class TrabajadorBase(BaseModel):
    nombre_trabajador: str = Field(min_length=1, max_length=100)
    peso_acumulado: int = Field(default=0)


class SoporteBase(BaseModel):
    nombre_soporte: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = Field(max_length=255)
    prioridad: int = Field(ge=1, le=5)
    peso_trabajo: int = Field(ge=1, le=5)


class AsignacionBase(BaseModel):
    id_trabajador: int
    id_soporte: int
    fecha_asignacion: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
