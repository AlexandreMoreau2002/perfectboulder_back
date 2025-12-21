from app.config import Settings
from app.services.health import build_database_config_payload, build_health_payload


def get_health(settings: Settings) -> dict[str, object]:
    return build_health_payload(settings)


def get_database_config(settings: Settings) -> dict[str, object]:
    return build_database_config_payload(settings)
