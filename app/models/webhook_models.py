import uuid
from typing import Optional, Dict, Any, List, Union, Literal
from pydantic import BaseModel, Field


# --- 기본 통화 정보 ---
class CallDetailsBase(BaseModel):
    agent_id: Optional[uuid.UUID] = Field(None, description="에이전트 고유 식별자")
    call_id: uuid.UUID = Field(..., description="통화 고유 식별자")
    call_type: Optional[str] = Field(None, description="통화 유형 (예: web, phone)")
    call_from: Optional[str] = Field(None, description="발신 번호 (있는 경우)")
    call_to: Optional[str] = Field(None, description="수신 번호 (있는 경우)")
    dynamic_variables: Optional[Dict[str, Any]] = Field(
        None, description="통화 시작 시 제공된 동적 변수"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="통화 관련 메타데이터")
    start_timestamp: Optional[int] = Field(
        None, description="통화 시작 시간 (Epoch milliseconds)"
    )
    opt_out_sensitive_data_storage: Optional[bool] = Field(
        None, description="민감 데이터 저장 비활성화 여부"
    )


# --- 통화 시작 페이로드 ---
class CallStartedDetails(CallDetailsBase):
    pass


class CallStartedPayload(BaseModel):
    event: Literal["call_started"] = Field(..., description="이벤트 유형: 통화 시작")
    call: CallStartedDetails = Field(..., description="통화 시작 상세 정보")


# --- 통화 종료 페이로드 ---
class TranscriptEntry(BaseModel):
    role: str = Field(..., description="참여자 역할 (예: agent, user)")
    content: str = Field(..., description="대화 내용")


class TranscriptToolCallEntry(BaseModel):
    role: Literal["tool_call_invocation", "tool_call_result"] = Field(
        ..., description="참여자 역할 (도구 호출 관련)"
    )
    tool_call_id: str = Field(..., description="도구 호출 고유 식별자")
    name: Optional[str] = Field(None, description="호출된 도구 이름")
    arguments: Optional[Dict[str, Any]] = Field(
        None, description="도구 호출 인수 (JSON 객체)"
    )
    content: Optional[str] = Field(None, description="도구 호출 결과 (JSON 문자열)")


class CallCost(BaseModel):
    total_credits_used: Optional[int] = Field(None, description="사용된 총 크레딧")
    duration_seconds: Optional[int] = Field(None, description="통화 시간 (초)")


class CustomAnalysisItem(BaseModel):
    type: str = Field(..., description="분석 데이터 유형 (예: string, boolean)")
    name: str = Field(..., description="분석 데이터 이름")
    value: Any = Field(..., description="분석 데이터 값")


class CallAnalysis(BaseModel):
    summary: Optional[str] = Field(None, description="통화 요약")
    user_sentiment: Optional[str] = Field(None, description="사용자 감성")
    custom_analysis_data: Optional[List[CustomAnalysisItem]] = Field(
        None, description="사용자 정의 분석 데이터 목록"
    )


class CallEndedDetails(CallDetailsBase):
    disconnection_reason: Optional[str] = Field(None, description="통화 종료 사유")
    end_timestamp: Optional[int] = Field(
        None, description="통화 종료 시간 (Epoch milliseconds)"
    )
    duration_ms: Optional[int] = Field(None, description="통화 시간 (밀리초)")
    transcript: Optional[List[TranscriptEntry]] = Field(
        None, description="통화 전체 대화 스크립트"
    )
    transcript_with_tool_calls: Optional[
        List[Union[TranscriptEntry, TranscriptToolCallEntry]]
    ] = Field(None, description="도구 호출 정보를 포함한 통화 대화 스크립트")
    recording_url: Optional[str] = Field(None, description="통화 녹음 파일 URL")
    call_cost: Optional[CallCost] = Field(None, description="통화 비용 정보")
    call_analysis: Optional[CallAnalysis] = Field(None, description="통화 분석 결과")

class MidCallDetails(BaseModel):
    agent_id: str = Field(..., description="에이전트 고유 식별자")
    call_id: str = Field(..., description="통화 고유 식별자")
    timestamp: int = Field(..., description="통화 시간 (Epoch milliseconds)")
    event_type: str = Field(..., description="이벤트 유형")
    event_data: Dict[str, Any] = Field(..., description="이벤트 데이터")


class CallEndedPayload(BaseModel):
    event: Literal["call_ended"] = Field(..., description="이벤트 유형: 통화 종료")
    call: CallEndedDetails = Field(..., description="통화 종료 상세 정보")

class MidCallPayload(BaseModel):
    event: Literal["mid_call"] = Field(..., description="이벤트 유형: 통화 중")
    mid_call: MidCallDetails = Field(..., description="통화 중 상세 정보")

# --- 통화 데이터 웹훅 엔드포인트를 위한 Union 타입 ---
CallWebhookPayload = Union[CallStartedPayload, CallEndedPayload, MidCallPayload]


# --- 인바운드 콜 웹훅 페이로드 ---
class InboundWebhookPayload(BaseModel):
    from_number: Optional[str] = Field(None, description="인바운드 콜 발신 번호")
    to_number: Optional[str] = Field(None, description="인바운드 콜 수신 번호")


class InboundCallDetailsResponse(BaseModel):
    dynamic_variables: Optional[Dict[str, Any]] = Field(
        None, description="에이전트에 전달할 동적 변수"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="통화에 연결할 메타데이터"
    )


class InboundWebhookResponse(BaseModel):
    call_inbound: InboundCallDetailsResponse = Field(
        ..., description="인바운드 콜 응답 상세 정보"
    )
