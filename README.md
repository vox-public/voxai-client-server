# 🎙️ VoxAI 연동 클라이언트 서버

> **Vox.ai와 쉽고 빠르게 연동하세요!** 🚀  
> 이 프로젝트는 고객사가 Vox.ai의 웹훅과 API 도구를 간편하게 연동할 수 있도록 만들어진 FastAPI 기반의 스타터 템플릿입니다.

## ✨ 왜 이 프로젝트를 사용해야 할까요?

- 🏃‍♂️ **빠른 시작**: 복잡한 설정 없이 5분 만에 Vox.ai 연동 시작
- 🔧 **쉬운 확장**: 깔끔한 구조로 새 기능 추가가 간단함
- 🛡️ **안전한 연동**: 보안 설정까지 고려된 완성형 템플릿

## 🎯 주요 기능

이 서버는 Vox.ai의 3가지 핵심 기능을 지원합니다:

### 1. 📞 통화 이벤트 웹훅
- **엔드포인트**: `/api/v1/call_events`
- **기능**: 통화 시작/종료 시 자동으로 알림이나 데이터 처리
- **예시**: 통화 종료 후 CRM에 자동 기록, Slack 알림 발송
- **📖 공식 문서**: [통화 데이터 웹훅 가이드](https://docs.tryvox.co/docs/monitor/webhook/webhook-overview)

### 2. 🔧 에이전트 도구 API
- **엔드포인트**: `/api/v1/tools/{tool_name}`
- **기능**: AI 에이전트가 대화 중 필요한 정보를 실시간으로 조회
- **예시**: 고객 정보 조회, 주문 상태 확인, 예약 처리
- **📖 공식 문서**: [API 도구 설정 가이드](https://docs.tryvox.co/docs/build/tools/api)

### 3. 📥 인바운드 콜 웹훅
- **엔드포인트**: `/api/v1/inbound`
- **기능**: 수신 전화에 맞춤형 정보 제공
- **예시**: 발신자별 개인화된 인사말, 고객 히스토리 기반 응대
- **📖 공식 문서**: [동적 변수 및 컨텍스트 주입](https://docs.tryvox.co/docs/build/context/dynamic-variables)

## 📁 프로젝트 구조

```
📦 voxai-client-server
├── 📄 README.md              # 👈 지금 보고 있는 파일
├── 🚀 main.py                # FastAPI 서버 시작점
├── ⚙️ pyproject.toml         # 프로젝트 설정 및 의존성
└── 📂 app/
    ├── 🌐 api/               # API 엔드포인트
    │   └── v1/endpoints/
    │       ├── agent_tools.py      # 🔧 AI 도구 API
    │       ├── call_webhooks.py    # 📞 통화 웹훅
    │       └── inbound_webhook.py  # 📥 인바운드 웹훅
    ├── ⚡ core/              # 핵심 설정
    │   ├── config.py         # 환경 설정
    │   ├── dependencies.py   # FastAPI DI 헬퍼
    │   └── logging.py        # 로그 설정
    ├── 📋 models/            # 데이터 모델
    │   ├── tool_models.py    # 도구 모델
    │   └── webhook_models.py # 웹훅 모델
    └── 🏗️ services/         # 비즈니스 로직
        ├── agent_tool_service.py
        ├── call_webhook_service.py
        ├── inbound_webhook_service.py
        └── handlers/         # 이벤트 처리기
            ├── base_handler.py
            ├── custom_url_handler.py
            ├── database_handler.py
            └── make_com_handler.py
```

## 🚀 5분 만에 시작하기

### 📋 준비물
- 🐍 **Python 3.8 이상**
- 📦 **Poetry** (의존성 관리 도구)

> 💡 **Poetry가 없다면?** `pip install poetry` 명령어로 설치하세요!

### 1️⃣ 프로젝트 다운로드

```bash
# 저장소 복제
git clone <repository_url>
cd voxai-client-server
```

### 2️⃣ 의존성 설치

```bash
# Poetry로 패키지 설치 (가상환경 자동 생성)
poetry install
```

### 3️⃣ 환경 설정

`.env` 파일을 만들어 필요한 설정을 입력하세요:

```bash
# .env 파일 생성
cp .env.example .env  # 예시 파일이 있다면
# 또는
touch .env
```

`.env` 파일 내용 예시:
```env
# 🎯 Make.com 연동 (선택사항)
MAKE_COM_WEBHOOK_URL="https://hook.us2.make.com/your-webhook-id"

# 🔗 커스텀 웹훅 URL (선택사항)
CUSTOM_SERVER_WEBHOOK_URL="https://your-server.com/webhook"

# 💾 데이터베이스 연결 (선택사항)
DATABASE_URL="postgresql://user:password@host:port/dbname"

# 🔁 웹훅 핸들러 토글 (선택사항)
CALL_WEBHOOK_HANDLERS__MAKE_COM_ENABLED=true
CALL_WEBHOOK_HANDLERS__CUSTOM_URL_ENABLED=true
CALL_WEBHOOK_HANDLERS__DATABASE_ENABLED=false
```

#### ⚙️ 구성 옵션 이해하기

- `environment`: `local`, `development`, `staging`, `production` 중 하나를 선택해 런타임 환경을 명시합니다. (기본값: `local`)
- `CALL_WEBHOOK_HANDLERS__*`: 콜 웹훅을 어느 채널로 전달할지 토글합니다. 값을 `false`로 설정하면 해당 핸들러가 등록되지 않습니다.
  - Make.com과 커스텀 URL 핸들러는 URL이 비어 있으면 자동으로 비활성화됩니다.
  - Database 핸들러는 `DATABASE_URL`이 필요합니다.
- 추가 환경 변수는 `.env`에 정의하면 FastAPI 시작 시 자동으로 로드됩니다. 더 많은 설정 키와 동작은 `app/core/config.py`에서 확인할 수 있습니다.

### 4️⃣ 서버 실행

```bash
# 개발 서버 시작 (코드 변경 시 자동 재시작)
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5️⃣ 성공 확인

서버가 정상 실행되면 이런 메시지가 나타납니다:

```
✅ INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✅ INFO:     Started reloader process [xxxxx]
✅ INFO:     Started server process [xxxxx]
✅ INFO:     Application startup complete.
```

이제 브라우저에서 **[http://localhost:8000/docs](http://localhost:8000/docs)** 로 접속해보세요!

## 🎨 API 문서 확인하기

서버가 실행되면 자동으로 생성되는 API 문서를 확인할 수 있습니다:

- 📖 **Swagger UI**: http://localhost:8000/docs
- 📋 **ReDoc**: http://localhost:8000/redoc

여기서 모든 API를 테스트하고 사용법을 확인할 수 있어요!

## 🔧 기능 확장하기

### 📞 새로운 웹훅 핸들러 추가

이 템플릿은 설정 기반으로 핸들러를 초기화합니다. 새로운 통합을 만들고 싶다면 다음 순서를 따르면 됩니다.

**1단계**: `app/services/handlers/` 아래에 새 핸들러 클래스를 추가합니다.
```python
from typing import Literal, Union

from app.core.logging import get_logger
from app.models.webhook_models import CallStartedPayload, CallEndedPayload
from .base_handler import BaseCallEventHandler

logger = get_logger(__name__)


class MyHandler(BaseCallEventHandler):
    async def handle(
        self,
        event_type: Literal["call_started", "call_ended"],
        payload: Union[CallStartedPayload, CallEndedPayload],
    ) -> None:
        logger.info("커스텀 핸들러 실행", extra={"event": event_type, "call_id": payload.call.call_id})
        # TODO: 실제 처리 로직 구현 (예: 외부 API 호출, DB 저장 등)
```

**2단계**: `CallWebhookHandlerSettings` 모델과 `_build_default_handlers` 메서드를 확장하여 새 핸들러에 대한 토글과 초기화 로직을 등록합니다.
```python
# app/core/config.py
class CallWebhookHandlerSettings(BaseModel):
    ...
    my_handler_enabled: bool = Field(default=False)

# app/services/call_webhook_service.py
from .handlers.my_handler import MyHandler

if handler_settings.my_handler_enabled:
    yield MyHandler()
```

**3단계**: `.env`에 토글 값을 추가하거나 기본값을 수정합니다.
```env
CALL_WEBHOOK_HANDLERS__MY_HANDLER_ENABLED=true
```

### 🔧 새로운 AI 도구 추가

고객 주문 상태를 조회하는 도구를 추가한다면:

**1단계**: `app/services/agent_tool_service.py`에 메서드 추가
```python
async def _handle_get_order_status(self, parameters: dict):
    order_id = parameters.get("order_id")
    # 주문 상태 조회 로직
    return {"status": "배송중", "tracking_number": "123456789"}
```

**2단계**: `process_tool_call` 메서드에 분기 추가
```python
elif tool_name == "get_order_status":
    return await self._handle_get_order_status(parameters)
```

## 🛡️ 보안 설정

Vox.ai와 안전하게 연동하기 위해 방화벽에서 다음 IP만 허용하세요:

```
🔒 Vox.ai 허용 IP: 34.123.198.226
```

**클라우드별 설정 방법:**
- **AWS**: Security Group에서 포트 8000에 해당 IP만 허용
- **GCP**: Firewall Rule에서 해당 IP 대역 허용
- **Azure**: Network Security Group에서 규칙 설정

## 📞 도움이 필요하신가요?

- 📧 **이메일**: support@tryvox.co
- 📚 **문서**: [Vox.ai 개발자 가이드](https://docs.tryvox.co/docs/intro/start)

---

**🎉 이제 Vox.ai와 연동을 시작할 준비가 완료되었습니다!**

궁금한 점이 있으시면 언제든 문의해 주세요. 즐거운 개발 되세요! 🚀 
