"""Dependency injection helpers for FastAPI routes."""
from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.agent_tool_service import AgentToolService
from app.services.call_webhook_service import CallWebhookService
from app.services.inbound_webhook_service import InboundWebhookService


def get_application_settings() -> Settings:
    """Provide cached application settings."""

    return get_settings()


def get_agent_tool_service(
    settings: Settings = Depends(get_application_settings),
) -> AgentToolService:
    return AgentToolService(settings=settings)


def get_call_webhook_service(
    settings: Settings = Depends(get_application_settings),
) -> CallWebhookService:
    return CallWebhookService(settings=settings)


def get_inbound_webhook_service(
    settings: Settings = Depends(get_application_settings),
) -> InboundWebhookService:
    return InboundWebhookService(settings=settings)
