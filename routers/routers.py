from typing import List
from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from config.database import SessionLocal
from fastapi.encoders import jsonable_encoder

from services.services import *
from schemas.schemas import *

from datetime import date


soporte_router = APIRouter()