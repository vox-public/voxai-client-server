from typing import Iterable, List, Optional, Sequence, Union, Literal

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.models.webhook_models import CallStartedPayload, CallEndedPayload
from .handlers.base_handler import BaseCallEventHandler
from .handlers.custom_url_handler import CustomUrlHandler
from .handlers.database_handler import DatabaseHandler
from .handlers.make_com_handler import MakeComHandler

logger = get_logger(__name__)


# 콜 데이터 웹훅 이벤트를 받아 여러 핸들러에게 전달하는 서비스
class CallWebhookService:

    def __init__(
        self,
        settings: Optional[Settings] = None,
        handlers: Optional[Sequence[BaseCallEventHandler]] = None,
    ):
        """핸들러 인스턴스를 초기화하고 등록합니다."""

        self._settings = settings or get_settings()
        self.handlers: List[BaseCallEventHandler] = list(
            handlers if handlers is not None else self._build_default_handlers()
        )

        if not self.handlers:
            logger.warning(
                "등록된 콜 웹훅 핸들러가 없습니다. 웹훅 이벤트를 무시합니다."
            )
        else:
            handler_names = ", ".join(
                handler.__class__.__name__ for handler in self.handlers
            )
            logger.info(
                "%s개의 핸들러로 CallWebhookService를 초기화했습니다: %s",
                len(self.handlers),
                handler_names,
            )

    def _build_default_handlers(self) -> Iterable[BaseCallEventHandler]:
        """Instantiate default handlers based on configuration."""

        handler_settings = self._settings.call_webhook_handlers

        if handler_settings.make_com_enabled and self._settings.make_com_webhook_url:
            yield MakeComHandler(settings=self._settings)
        elif handler_settings.make_com_enabled:
            logger.warning(
                "Make.com 핸들러가 활성화되었지만 웹훅 URL이 설정되지 않았습니다."
            )

        if handler_settings.database_enabled and self._settings.database_url:
            yield DatabaseHandler(settings=self._settings)
        elif handler_settings.database_enabled:
            logger.warning(
                "Database 핸들러가 활성화되었지만 DATABASE_URL이 설정되지 않았습니다."
            )

        if (
            handler_settings.custom_url_enabled
            and self._settings.custom_server_webhook_url
        ):
            yield CustomUrlHandler(settings=self._settings)
        elif handler_settings.custom_url_enabled:
            logger.warning(
                "커스텀 URL 핸들러가 활성화되었지만 CUSTOM_SERVER_WEBHOOK_URL이 설정되지 않았습니다."
            )

    async def process_webhook_event(
        self,
        event_type: Literal["call_started", "call_ended"],
        payload: Union[CallStartedPayload, CallEndedPayload],
    ):
        """
        받은 웹훅 이벤트를 등록된 모든 핸들러에게 전달합니다.
        각 핸들러는 순차적으로 실행됩니다.
        """
        if not self.handlers:
            logger.info("통화 웹훅 이벤트를 처리할 핸들러가 없어 요청을 건너뜁니다.")
            return {"message": "활성화된 핸들러가 없어 이벤트를 건너뜁니다."}

        logger.info(f"통화 웹훅 이벤트 처리 시작: {event_type}")

        # 순차 실행 (디버깅 및 로깅에 더 용이할 수 있음)
        for handler in self.handlers:
            handler_name = handler.__class__.__name__
            try:
                logger.info(f"핸들러 실행: {handler_name} (이벤트: {event_type})")
                await handler.handle(event_type, payload)
                logger.info(f"핸들러 {handler_name} 실행 완료 (이벤트: {event_type})")
            except Exception as e:
                # 특정 핸들러 실패가 전체 요청을 중단시키지 않도록 예외 처리
                logger.error(
                    f"핸들러 {handler_name} 실행 중 오류 발생 (이벤트: {event_type}): {e}"
                )

        logger.info(f"통화 웹훅 이벤트 처리 완료: {event_type}")

        return {
            "message": f"통화 웹훅 이벤트 '{event_type}'가 서비스에 의해 처리되었습니다."
        }
