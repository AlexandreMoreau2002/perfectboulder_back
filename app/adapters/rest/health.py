from fastapi import APIRouter, Depends

from app.application.health.service import get_database_config, get_health_status
from app.config import Settings, get_settings

router = APIRouter()


@router.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return get_health_status(settings)


@router.get("/database/config")
def database_config(settings: Settings = Depends(get_settings)):
    return get_database_config(settings)
