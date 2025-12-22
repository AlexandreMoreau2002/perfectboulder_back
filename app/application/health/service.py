from dataclasses import asdict

from app.config import Settings
from app.domain.health.entities import DatabaseConfigView, HealthStatus


def get_health_status(settings: Settings) -> dict[str, object]:
    payload = HealthStatus(status="ok", service=settings.app_name)
    return {
        "error": False,
        "message": "Service healthy",
        "data": asdict(payload),
    }


def get_database_config(settings: Settings) -> dict[str, object]:
    payload = DatabaseConfigView(database_url=settings.safe_database_url)
    return {
        "error": False,
        "message": "Database configuration",
        "data": asdict(payload),
    }
