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

**또는 직접 실행:**
```bash
uv run inspect eval examples/01_hello_world.py --model openai/gpt-4o
```

## 모든 예제

```bash
# 간단한 방법 (추천)
uv run python run.py 01  # Hello World
uv run python run.py 02  # Security Guide  
uv run python run.py 03  # Multiple Choices (HellaSwag, 50개 샘플)
uv run python run.py 04  # Mathematics (GSM8K, 50개 샘플)

# 직접 실행하는 방법 (Python 파일 직접 지정)
uv run inspect eval examples/01_hello_world.py --model openai/gpt-4o
uv run inspect eval examples/02_security_guide.py --model openai/gpt-4o
uv run inspect eval examples/03_multiple_choices.py --model openai/gpt-4o --limit 50
uv run inspect eval examples/04_mathematics.py --model openai/gpt-4o --limit 50

# 다른 모델로 실행
uv run python run.py 01 --model gpt-4o-mini
uv run python run.py 03 --model anthropic/claude-3-5-sonnet-20241022
```

## 참고 자료

- [Inspect AI 공식 문서](https://inspect.ai-safety-institute.org.uk/)
- [Inspect AI GitHub](https://github.com/UKGovernmentBEIS/inspect_ai)
