from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.config import get_settings
from app.adapters.graphql.schema import create_schema
from app.adapters.rest.health import router as health_router
from app.infra.database.probe import ensure_database_ready


def create_app() -> FastAPI:
    settings = get_settings()

    graphql_app = GraphQLRouter(create_schema(settings))

    application = FastAPI(title=settings.app_name)

    application.include_router(health_router)
    application.include_router(graphql_app, prefix="/graphql")

    @application.on_event("startup")
    async def _startup_database_check() -> None:
        await ensure_database_ready(settings)

    return application


app = create_app()
