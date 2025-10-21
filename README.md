# Inspect AI Guide KO

Inspect AI 프레임워크 학습 및 테스트를 위한 저장소입니다.

## 빠른 시작

### 1. UV 설치

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 확인:
```bash
uv --version
```

### 2. 의존성 설치

```bash
uv sync
```

### 3. API 키 설정

```bash
# .env 파일 생성
cp env.example .env

# .env 파일 편집하여 OpenAI API 키 입력
# OPENAI_API_KEY=your-api-key-here
```

> API 키 발급: https://platform.openai.com/api-keys

### 4. 첫 예제 실행

**간단하게 실행 (권장):**
```bash
uv run python run.py 01
```

**사용 가능한 예제 목록 보기:**
```bash
uv run python run.py --list
```

## 모든 예제

```bash
# 간단한 방법 (추천)
uv run python run.py 01  # Hello World
uv run python run.py 02  # Security Guide  
uv run python run.py 03  # Multiple Choices (HellaSwag, 50개 샘플)
uv run python run.py 04  # Mathematics (GSM8K, 50개 샘플)
uv run python run.py 05  # Tool Use
uv run python run.py 06  # Custom Grader Instance
uv run python run.py 07  # Custom Grader Template
uv run python run.py 08  # Multi Turn
uv run python run.py 09  # JSON
uv run python run.py 10  # All Attack Test
```

## 모델 설정

모든 모델 설정은 `config.yaml` 파일에서 관리됩니다:

```yaml
# 기본 모델 설정
default_model: openai/gpt-4o

# 예제별 개별 설정
examples:
  "01":
    name: "Hello World"
    task: examples/01_hello_world.py
    model: openai/gpt-4o  # 이 예제만 다른 모델 사용 가능
    options: []
```

모델을 변경하려면 `config.yaml` 파일을 편집하세요.

## 참고 자료

- [Inspect AI 공식 문서](https://inspect.ai-safety-institute.org.uk/)
- [Inspect AI GitHub](https://github.com/UKGovernmentBEIS/inspect_ai)
