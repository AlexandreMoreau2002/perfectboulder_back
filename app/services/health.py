from app.config import Settings


def build_health_payload(settings: Settings) -> dict[str, object]:
    return {
        "error": False,
        "message": "Service healthy",
        "data": {
            "status": "ok",
            "service": settings.app_name,
        },
    }


def build_database_config_payload(settings: Settings) -> dict[str, object]:
    return {
        "error": False,
        "message": "Database configuration",
        "data": {"database_url": settings.safe_database_url},
    }
