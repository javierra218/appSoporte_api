from sqlalchemy import Column as Col, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Trabajador(Base):
    __tablename__ = 'trabajadores'
    
    id_trabajador = Col(Integer, primary_key=True, index=True)
    nombre_trabajador = Col(VARCHAR(100))
    peso_acumulado = Col(Integer, default=0)

    # Relación con Asignacion
    asignaciones = relationship("Asignacion", back_populates="trabajador")

class Soporte(Base):
    __tablename__ = 'soportes'
    
    id_soporte = Col(Integer, primary_key=True, index=True)
    nombre_soporte = Col(VARCHAR(100))
    descripcion = Col(VARCHAR(255))
    prioridad = Col(Integer)
    peso_trabajo = Col(Integer)

    # Relación con Asignacion
    asignaciones = relationship("Asignacion", back_populates="soporte")

class Asignacion(Base):
    __tablename__ = 'asignaciones'
    
    id_asignacion = Col(Integer, primary_key=True, index=True)
    id_trabajador = Col(Integer, ForeignKey('trabajadores.id_trabajador'))
    id_soporte = Col(Integer, ForeignKey('soportes.id_soporte'))
    fecha_asignacion = Col(DateTime(timezone=True), server_default=func.now())

    # Relación con Trabajador y Soporte
    trabajador = relationship("Trabajador", back_populates="asignaciones")
    soporte = relationship("Soporte", back_populates="asignaciones")
