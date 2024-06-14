# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse

# from middlewares.error_handler import ErrorHandler

# from config.database import engine, Base

# from routers.routers import soporte_router

# app = FastAPI()
# app.title = "appSoportes"

# app.add_middleware(ErrorHandler)
# app.include_router(soporte_router)

# Base.metadata.create_all(bind=engine)  # Crear las tablas en la base de datos

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     return "<h1>appSoportes</h1>"


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from config.database import engine, Base, SessionLocal
from services.services import TrabajadorService
from routers.routers import soporte_router
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "appSoportes"

app.add_middleware(ErrorHandler)
app.include_router(soporte_router)

Base.metadata.create_all(bind=engine)  # Crear las tablas en la base de datos

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>appSoportes</h1>"

# Función para reiniciar los pesos acumulados
def reset_pesos_acumulados():
    db = SessionLocal()
    trabajador_service = TrabajadorService(db)
    trabajador_service.reset_pesos_acumulados()
    db.close()
    print("Pesos acumulados reseteados.")

# Configurar el scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=0, minute=0)  # Ejecutar a medianoche todos los días
scheduler.add_job(reset_pesos_acumulados, trigger)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar el scheduler
    scheduler.start()
    print("Scheduler iniciado")
    
    yield
    
    # Detener el scheduler al finalizar la aplicación
    scheduler.shutdown()
    print("Scheduler detenido")

app.router.lifespan_context = lifespan
