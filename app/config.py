from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    app_name: str = Field(default="Backend API", env=["APP_NAME", "BACKEND_APP_NAME"])
    database_url: str | None = Field(
        default=None,
        env=["DATABASE_URL", "BACKEND_DATABASE_URL"],
    )
    database_host: str = Field(
        default="db",
        env=["DB_HOST", "BACKEND_DATABASE_HOST", "DATABASE_HOST"],
    )
    database_port: int = Field(
        default=5432,
        env=["DB_PORT", "BACKEND_DATABASE_PORT", "DATABASE_PORT"],
    )
    database_user: str = Field(
        default="perfectboulder",
        env=["DB_USER", "BACKEND_DATABASE_USER", "DATABASE_USER"],
    )
    database_password: str = Field(
        default="perfectboulder",
        env=["DB_PASSWORD", "BACKEND_DATABASE_PASSWORD", "DATABASE_PASSWORD"],
    )
    database_name: str = Field(
        default="perfectboulder",
        env=["DB_NAME", "BACKEND_DATABASE_NAME", "DATABASE_NAME"],
    )

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        return (
            f"postgresql://{self.database_user}:"
            f"{self.database_password}@"
            f"{self.database_host}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

    @property
    def safe_database_url(self) -> str:
        url = self.resolved_database_url
        parsed = urlsplit(url)

        if parsed.username is None:
            return url

        masked_password = "******" if parsed.password else None
        netloc = parsed.hostname or ""

        if parsed.username:
            credentials = parsed.username
            if masked_password is not None:
                credentials = f"{credentials}:{masked_password}"
            netloc = f"{credentials}@{netloc}"

        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"

        return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))


@lru_cache
def get_settings() -> Settings:
    return Settings()
