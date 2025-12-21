import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.config import get_settings
from app.routes.health import router as health_router
from app.services.database import ensure_database_ready


def create_app() -> FastAPI:
    settings = get_settings()

    @strawberry.type
    class Query:
        @strawberry.field
        def status(self) -> str:
            return "ok"

        @strawberry.field
        def service_name(self) -> str:
            return settings.app_name

        @strawberry.field
        def database_dsn(self) -> str:
            return settings.safe_database_url

    graphql_app = GraphQLRouter(strawberry.Schema(Query))

    application = FastAPI(title=settings.app_name)

    application.include_router(health_router)
    application.include_router(graphql_app, prefix="/graphql")

    @application.on_event("startup")
    async def _startup_database_check() -> None:
        await ensure_database_ready(settings)

    return application


app = create_app()
