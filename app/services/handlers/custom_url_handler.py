from typing import Literal, Optional, Union

import httpx

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.models.webhook_models import CallEndedPayload, CallStartedPayload
from .base_handler import BaseCallEventHandler

logger = get_logger(__name__)


# 커스텀 서버 URL로 데이터를 전송하는 핸들러
class CustomUrlHandler(BaseCallEventHandler):

    def __init__(self, settings: Optional[Settings] = None):
        self._settings = settings or get_settings()

    async def handle(
        self,
        event_type: Literal["call_started", "call_ended"],
        payload: Union[CallStartedPayload, CallEndedPayload],
    ):
        """
        콜 데이터 웹훅 페이로드를 사용자가 지정한 커스텀 서버 URL로 전송합니다.
        설정된 CUSTOM_SERVER_WEBHOOK_URL이 없으면 아무것도 하지 않습니다.
        """
        webhook_url = self._settings.custom_server_webhook_url
        if not webhook_url:
            logger.warning("커스텀 서버 웹훅 URL이 설정되지 않아 스킵합니다.")
            return

        logger.info(f"{event_type} 이벤트를 커스텀 서버 웹훅으로 전송합니다...")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url, json=payload.model_dump(mode="json"), timeout=10.0
                )
                response.raise_for_status()

            logger.info(
                f"{event_type} 이벤트를 커스텀 서버로 성공적으로 전송했습니다. 상태: {response.status_code}"
            )

        except httpx.HTTPStatusError as e:
            logger.error(
                f"커스텀 서버로 {event_type} 전송 중 HTTP 오류 발생: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"커스텀 서버로 {event_type} 전송 중 요청 오류 발생: {e}")
        except Exception as e:
            logger.error(
                f"커스텀 서버로 {event_type} 전송 중 예기치 않은 오류 발생: {e}"
            )
