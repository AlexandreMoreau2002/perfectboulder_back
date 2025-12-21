from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.controllers.health import get_database_config, get_health

router = APIRouter()


@router.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return get_health(settings)


@router.get("/database/config")
def database_config(settings: Settings = Depends(get_settings)):
    return get_database_config(settings)
