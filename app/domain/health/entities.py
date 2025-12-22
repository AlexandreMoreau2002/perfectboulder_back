from dataclasses import dataclass


@dataclass(slots=True)
class HealthStatus:
    status: str
    service: str


@dataclass(slots=True)
class DatabaseConfigView:
    database_url: str
