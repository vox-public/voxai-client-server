from functools import lru_cache
from typing import Literal, Optional

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CallWebhookHandlerSettings(BaseModel):
    """Toggles for webhook handlers."""

    make_com_enabled: bool = Field(
        default=True, description="Enable forwarding call events to Make.com",
    )
    custom_url_enabled: bool = Field(
        default=True, description="Enable forwarding call events to a custom URL",
    )
    database_enabled: bool = Field(
        default=False,
        description="Enable persistence of call events to a database (requires DATABASE_URL)",
    )


class Settings(BaseSettings):
    """Application settings"""

    environment: Literal["local", "development", "staging", "production"] = "local"
    make_com_webhook_url: Optional[AnyHttpUrl] = None
    custom_server_webhook_url: Optional[AnyHttpUrl] = None
    database_url: Optional[str] = None  # Example DB URL
    call_webhook_handlers: CallWebhookHandlerSettings = CallWebhookHandlerSettings()

    # Configuration for Pydantic Settings (loads from .env)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> "Settings":
    """Return cached application settings."""

    return Settings()


# Backwards-compatible module-level export for legacy imports
settings = get_settings()
