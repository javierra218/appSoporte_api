from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from middlewares.error_handler import ErrorHandler

from config.database import engine, Base

from routers.routers import soporte_router

app = FastAPI()
app.title = "appSoportes"

app.add_middleware(ErrorHandler)
app.include_router(soporte_router)

Base.metadata.create_all(bind=engine)  # Crear las tablas en la base de datos

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>appSoportes</h1>"