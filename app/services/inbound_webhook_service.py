from typing import Any, Dict, Optional

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.models.webhook_models import (
    InboundWebhookPayload,
    InboundWebhookResponse,
    InboundCallDetailsResponse,
)

logger = get_logger(__name__)


# 인바운드 콜 웹훅을 처리하는 서비스
class InboundWebhookService:

    def __init__(self, settings: Optional[Settings] = None):
        self._settings = settings or get_settings()

    async def process_inbound_call(
        self, payload: InboundWebhookPayload
    ) -> InboundWebhookResponse:
        """
        인바운드 콜 웹훅 요청을 처리하고 동적 변수 및 메타데이터를 반환합니다.
        발신 번호 등을 기반으로 사용자 정보를 조회하는 로직을 여기에 추가합니다.
        """
        logger.info(f"인바운드 콜 웹훅 처리 시작, 페이로드: {payload}")

        from_number = payload.call_inbound.from_number
        to_number = payload.call_inbound.to_number

        dynamic_variables: Dict[str, Any] = {}
        metadata: Dict[str, Any] = {}

        # --- 예시 로직: 발신 번호에 따라 동적 변수 설정 ---
        if from_number == "821012345678":
            dynamic_variables["user_name"] = "김철수"
            dynamic_variables["product_name"] = "아이폰 16 프로"
            metadata["user_id"] = "user_kim_chul_su_123"
            logger.info(f"{from_number}로부터 김철수님을 식별했습니다.")
        elif from_number == "821087654321":
            dynamic_variables["user_name"] = "손예진"
            dynamic_variables["last_order_date"] = "2024-07-01"
            metadata["user_id"] = "user_son_ye_jin_456"
            logger.info(f"{from_number}로부터 손예진님을 식별했습니다.")
        else:
            dynamic_variables["user_name"] = "고객님"  # 기본 이름
            logger.info(f"알 수 없는 발신 번호: {from_number}. 기본 이름을 사용합니다.")
            # 알 수 없는 번호 처리 로직 (예: 신규 고객 처리)

        # 데이터베이스 조회, 외부 API 호출 등 복잡한 로직 추가 가능

        response_data = InboundCallDetailsResponse(
            dynamic_variables=dynamic_variables, metadata=metadata
        )

        logger.info(f"인바운드 콜 처리 완료, 반환 데이터: {response_data}")
        return InboundWebhookResponse(call_inbound=response_data)
