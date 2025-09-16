from fastapi import APIRouter, Body, Depends, HTTPException, Path

from app.core.dependencies import get_agent_tool_service
from app.core.logging import get_logger
from app.models.tool_models import AgentToolRequestPayload, AgentToolResponsePayload
from app.services.agent_tool_service import AgentToolService

logger = get_logger(__name__)
router = APIRouter()


# 에이전트 도구 호출을 수신하는 동적 엔드포인트
# tool_name 경로 변수에 따라 다른 도구 호출을 처리할 수 있습니다.
@router.post(
    "/tools/{tool_name}",
    summary="에이전트 도구 호출 처리",
    response_model=AgentToolResponsePayload,
    response_description="도구 실행 결과",
)
async def handle_agent_tool(
    tool_name: str = Path(..., description="호출할 도구의 이름"),
    payload: AgentToolRequestPayload = Body(
        ..., description="도구 호출에 필요한 파라미터 (JSON 객체)"
    ),
    agent_tool_service: AgentToolService = Depends(get_agent_tool_service),
) -> AgentToolResponsePayload:
    """
    Vox.ai 에이전트로부터 특정 API 도구 호출을 수신하고 처리합니다.
    `tool_name` 경로는 Vox.ai 대시보드에 설정된 도구 이름과 일치해야 합니다.
    요청 본문은 해당 도구의 설정에 정의된 파라미터 스키마를 따릅니다.
    """
    logger.info(f"수신된 에이전트 도구 호출: '{tool_name}', 페이로드: {payload}")

    # 서비스에게 도구 호출 처리를 위임합니다.
    try:
        response_data = await agent_tool_service.process_tool_call(tool_name, payload)
        return response_data
    except Exception as e:
        logger.error(f"에이전트 도구 '{tool_name}' 처리 중 오류 발생: {e}")
        # 실제 프로덕션에서는 도구 실행 실패에 대한 사용자 친화적인 응답 형식을 정의해야 합니다.
        raise HTTPException(status_code=500, detail=f"도구 처리 중 오류 발생: {e}")
