from fastapi import APIRouter, Depends

from app.core.dependencies import get_inbound_webhook_service
from app.core.logging import get_logger
from app.models.webhook_models import InboundWebhookPayload, InboundWebhookResponse
from app.services.inbound_webhook_service import InboundWebhookService

logger = get_logger(__name__)
router = APIRouter()


# 인바운드 콜 웹훅을 수신하는 엔드포인트
# 발신 번호 등을 기반으로 동적 변수를 설정하여 응답합니다.
@router.post(
    "/inbound",
    summary="인바운드 콜 웹훅 수신",
    response_model=InboundWebhookResponse,
    response_description="동적 변수 및 메타데이터",
)
async def handle_inbound_webhook(
    webhook_data: InboundWebhookPayload,  # Pydantic 모델을 사용하여 자동 유효성 검사 및 파싱
    inbound_webhook_service: InboundWebhookService = Depends(
        get_inbound_webhook_service
    ),
) -> InboundWebhookResponse:
    """
    Vox.ai로부터 인바운드 콜 웹훅 이벤트를 수신합니다.
    이 웹훅은 통화 라우팅 또는 에이전트에게 전달할 정보를 동적으로 설정하는 데 사용됩니다.
    응답으로 동적 변수와 메타데이터를 반환하여 통화 처리에 활용할 수 있습니다.
    """
    logger.info(f"수신된 인바운드 웹훅 이벤트: {webhook_data}")

    # 서비스에게 인바운드 콜 처리를 위임하고 응답을 반환합니다.
    response_data = await inbound_webhook_service.process_inbound_call(webhook_data)
    return response_data
