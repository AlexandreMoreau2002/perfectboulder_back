import strawberry

from app.application.health.service import get_database_config, get_health_status
from app.config import Settings


def create_schema(settings: Settings) -> strawberry.Schema:
    @strawberry.type
    class Query:
        @strawberry.field
        def status(self) -> str:
            payload = get_health_status(settings)
            return str(payload["data"]["status"])

        @strawberry.field
        def service_name(self) -> str:
            payload = get_health_status(settings)
            return str(payload["data"]["service"])

        @strawberry.field
        def database_dsn(self) -> str:
            payload = get_database_config(settings)
            return str(payload["data"]["database_url"])

    return strawberry.Schema(Query)
