from datetime import datetime, timezone
from typing import Literal, Optional, Union

import httpx

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.models.webhook_models import CallEndedPayload, CallStartedPayload
from .base_handler import BaseCallEventHandler

logger = get_logger(__name__)


# Make.com 웹훅으로 데이터를 전송하는 핸들러
class MakeComHandler(BaseCallEventHandler):

    def __init__(self, settings: Optional[Settings] = None):
        self._settings = settings or get_settings()

    async def handle(
        self,
        event_type: Literal["call_started", "call_ended"],
        payload: Union[CallStartedPayload, CallEndedPayload],
    ):
        """
        콜 데이터 웹훅 페이로드를 Make.com 웹훅 URL로 전송합니다.
        설정된 MAKE_COM_WEBHOOK_URL이 없으면 아무것도 하지 않습니다.
        """
        webhook_url = self._settings.make_com_webhook_url
        if not webhook_url:
            logger.warning("Make.com 웹훅 URL이 설정되지 않아 스킵합니다.")
            return

        # --- Make.com 전용 페이로드 생성 로직 (시작) ---
        # 기존 payload 데이터를 사용해서 Make.com에 최적화된 새로운 payload를 생성합니다.
        # 이 로직을 주석 처리하거나 필요에 맞게 수정하여 사용하세요.

        # 기본 Make.com 페이로드 구조
        send_payload = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if event_type == "call_started" and isinstance(payload, CallStartedPayload):
            call = payload.call
            send_payload.update(
                {
                    "call_id": str(call.call_id),
                    "agent_id": str(call.agent_id) if call.agent_id else None,
                    "call_from": call.call_from,
                    "call_to": call.call_to,
                    "dynamic_variables": call.dynamic_variables,
                }
            )

        elif event_type == "call_ended" and isinstance(payload, CallEndedPayload):
            agent_id = payload.call.agent_id

            # 기본 call_ended 페이로드
            send_payload.update(
                {
                    "call_id": str(payload.call.call_id),
                    "agent_id": str(agent_id) if agent_id else None,
                    "disconnection_reason": payload.call.disconnection_reason,
                    "duration_ms": payload.call.duration_ms,
                    "call_from": payload.call.call_from,
                    "call_to": payload.call.call_to,
                }
            )

            # 특정 agent_id에 대한 커스텀 페이로드 구조
            if agent_id and str(agent_id) == "e15cf4cb-08ca-4832-b528-9a2cd45decb6":
                logger.info(
                    f"Creating custom Make.com payload for agent_id: {agent_id}"
                )

                # 완전히 새로운 Make.com 전용 페이로드 구조
                send_payload = {
                    "event_type": "custom_call_ended",
                    "call_id": str(payload.call.call_id),
                    "disconnection_reason": payload.call.disconnection_reason,
                    "customer_name": (
                        payload.call.dynamic_variables.get("customer_name")
                        if payload.call.dynamic_variables
                        else None
                    ),
                    "processed_at": datetime.now(timezone.utc).isoformat(),
                    "agent_id": str(agent_id),
                }
        else:
            logger.warning("지원하지 않는 이벤트 유형 %s로 Make.com 핸들러를 호출했습니다.", event_type)
            return

        # --- Make.com 전용 페이로드 생성 로직 (끝) ---

        logger.info(f"{event_type} 이벤트를 Make.com 웹훅으로 전송합니다...")

        try:
            # Pydantic 모델을 dict로 변환하여 전송
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=send_payload,
                    timeout=10.0,  # 타임아웃 설정 (초)
                )
                response.raise_for_status()  # 4xx/5xx 상태 코드에 대해 예외 발생

            logger.info(
                f"{event_type} 이벤트를 Make.com으로 성공적으로 전송했습니다. 상태: {response.status_code}"
            )

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Make.com으로 {event_type} 전송 중 HTTP 오류 발생: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Make.com으로 {event_type} 전송 중 요청 오류 발생: {e}")
        except Exception as e:
            logger.error(
                f"Make.com으로 {event_type} 전송 중 예기치 않은 오류 발생: {e}"
            )
