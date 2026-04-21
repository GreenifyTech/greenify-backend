import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_ENV_PATH, override=False)


def _get_env(name: str, default: str | None = None, *, required: bool = False) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        if required and default is None:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return default
    return value


def _get_int(name: str, default: int, *, required: bool = False) -> int:
    value = _get_env(name, None, required=required)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid int for {name}") from exc


def _get_bool(name: str, default: bool) -> bool:
    value = _get_env(name, None, required=False)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    app_name: str
    debug: bool
    frontend_url: str

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @classmethod
    def from_env(cls) -> "Settings":
        debug = _get_bool("DEBUG", False)
        if not debug:
            debug = _get_bool("APP_DEBUG", False)

        return cls(
            db_host=_get_env("DB_HOST", "localhost", required=True) or "localhost",
            db_port=_get_int("DB_PORT", 3306, required=True),
            db_name=_get_env("DB_NAME", "greenify_db", required=True) or "greenify_db",
            db_user=_get_env("DB_USER", "root", required=True) or "root",
            db_password=_get_env("DB_PASSWORD", "", required=True) or "",
            secret_key=_get_env("SECRET_KEY", "", required=True) or "",
            algorithm=_get_env("ALGORITHM", "HS256") or "HS256",
            access_token_expire_minutes=_get_int("ACCESS_TOKEN_EXPIRE_MINUTES", 1440),
            app_name=_get_env("APP_NAME", "Greenify API") or "Greenify API",
            debug=debug,
            frontend_url=_get_env("FRONTEND_URL", "http://localhost:5173")
            or "http://localhost:5173",
        )


settings = Settings.from_env()
