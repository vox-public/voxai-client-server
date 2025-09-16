from typing import Literal, Optional, Union

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.models.webhook_models import CallEndedPayload, CallStartedPayload
from .base_handler import BaseCallEventHandler

logger = get_logger(__name__)


# 데이터베이스에 통화 데이터를 저장하는 핸들러
class DatabaseHandler(BaseCallEventHandler):

    def __init__(self, settings: Optional[Settings] = None):
        self._settings = settings or get_settings()

    async def handle(
        self,
        event_type: Literal["call_started", "call_ended"],
        payload: Union[CallStartedPayload, CallEndedPayload],
    ):
        """
        콜 데이터 웹훅 페이로드를 데이터베이스에 저장합니다.
        이 함수는 스켈레톤 구현이며, 실제 데이터베이스 로직으로 확장해야 합니다.
        """
        if not self._settings.database_url:
            logger.warning("데이터베이스 URL이 설정되지 않아 DB 저장을 스킵합니다.")
            return

        logger.info(f"{event_type} 이벤트를 데이터베이스에 저장하려고 시도합니다...")
        logger.info(
            "이곳에 데이터베이스 연결 및 저장 로직을 구현하세요 (예: SQLAlchemy, Tortoise ORM 사용)."
        )

        try:
            # --- 실제 데이터베이스 저장 로직을 여기에 구현 ---
            # 예시: call_id와 event_type을 로그로 남깁니다.
            call_id = payload.call.call_id
            logger.info(
                f"성공적으로 처리 (예시): Call ID '{call_id}'의 '{event_type}' 이벤트를 DB에 저장했습니다."
            )
            # ------------------------------------------------

        except Exception as e:
            logger.error(
                f"데이터베이스에 {event_type} 저장 중 예기치 않은 오류 발생: {e}"
            )
