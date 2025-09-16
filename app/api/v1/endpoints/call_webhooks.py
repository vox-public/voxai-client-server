from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_call_webhook_service
from app.core.logging import get_logger
from app.models.webhook_models import CallWebhookPayload
from app.services.call_webhook_service import CallWebhookService

logger = get_logger(__name__)
router = APIRouter()


# 통화 데이터 웹훅 이벤트를 수신하는 엔드포인트
# call_started 및 call_ended 이벤트를 모두 처리합니다.
@router.post(
    "/call_events",
    summary="통화 데이터 웹훅 수신",
    response_description="이벤트 처리 결과",
)
async def handle_call_webhook(
    webhook_data: CallWebhookPayload,  # Pydantic 모델을 사용하여 자동 유효성 검사 및 파싱
    call_webhook_service: CallWebhookService = Depends(get_call_webhook_service),
) -> Dict[str, Any]:
    """
    Vox.ai로부터 통화 시작(`call_started`) 또는 통화 종료(`call_ended`) 이벤트를 수신합니다.
    수신된 이벤트는 내부 서비스에 의해 여러 핸들러(Make.com 전송, DB 저장 등)로 분배됩니다.
    """
    event_type = webhook_data.event
    logger.info(f"수신된 통화 웹훅 이벤트: {event_type}")

    # 서비스에게 이벤트 처리를 위임합니다.
    try:
        result = await call_webhook_service.process_webhook_event(
            event_type, webhook_data
        )
        return {
            "status": "success",
            "message": f"웹훅 이벤트 '{event_type}'가 수신되어 처리를 시작합니다.",
            "details": result.get("message", ""),
        }
    except Exception as e:
        logger.error(f"통화 웹훅 이벤트 {event_type} 처리 중 오류 발생: {e}")
        # 실제 프로덕션에서는 더 구체적인 오류 처리가 필요합니다.
        raise HTTPException(
            status_code=500, detail=f"웹훅 처리 중 내부 서버 오류 발생: {e}"
        )
