# Inspect AI Guide KO

**Inspect AI**는 AI 모델의 성능과 안전성을 체계적으로 평가하기 위한 오픈소스 프레임워크입니다.  
이 저장소는 Inspect AI의 핵심 기능을 학습하고 실습할 수 있는 한국어 가이드와 예제를 제공합니다.

## 1. 프로젝트 구조

```
inspect-ai-guide-ko/
├── run.py                 # 통합 실행 스크립트
├── config.yaml            # 모든 설정 관리 (모델, 옵션 등)
├── examples/              # 예제 파일 디렉토리
│   ├── 01_hello_world.py
│   ├── 02_security_guide.py
│   ├── 03_multiple_choices.py
│   ├── 04_mathematics.py
│   ├── 05_tool_use.py
│   ├── 06_custom_grader_inst.py
│   ├── 07_custom_grader_template.py
│   ├── 08_multi_turn.py
│   └── 09_json.py
├── data/                  # 예제 데이터 파일
│   └── attack_sample.json
├── logs/                  # 실행 로그 저장 디렉토리
├── .env                   # API 키 저장 (gitignore됨)
├── pyproject.toml         # 프로젝트 의존성
└── README.md              # 이 파일
```

### 1.1. 주요 파일 설명

- **`run.py`**: 모든 예제를 간편하게 실행할 수 있는 통합 스크립트
  - 예제 목록 조회 (`--list`)
  - 상세 도움말 확인 (`--help`)
  - 번호로 간편 실행 (`uv run python run.py 01`)

- **`config.yaml`**: 중앙 집중식 설정 관리
  - 기본 모델 설정
  - 예제별 개별 모델 및 옵션
  - 로그 디렉토리 경로
  - 샘플 개수 제한 등

### 1.2. Examples 설명

**01_hello_world.py**
- 가장 단순한 평가 태스크 작성 방법

**02_security_guide.py**
- `system_message`로 AI 행동 규칙 설정
- `model_graded_fact`로 다른 AI가 답변 평가

**03_multiple_choices.py**
- HuggingFace 데이터셋(HellaSwag) 활용한 객관식 문제 평가
- `multiple_choice` solver와 `choice` scorer 사용

**04_mathematics.py**
- GSM8K 수학 문제 데이터셋으로 수치 계산 능력 평가
- `prompt_template`으로 답변 형식 지정, `match(numeric=True)`로 숫자 비교

**05_tool_use.py**
- `@tool` 데코레이터로 Python 함수를 AI가 호출 가능한 도구로 변환
- `use_tools`로 AI에게 함수 실행 권한 부여

**06_custom_grader_inst.py**
- `model_graded_qa`의 `instructions` 파라미터로 간단한 채점 기준 커스터마이징
- 기본 템플릿을 유지하면서 평가 기준만 변경

**07_custom_grader_template.py**
- `template`과 `instructions` 모두 커스터마이징하여 평가 프롬프트 전체 구조 설계
- 템플릿 변수(`{question}`, `{answer}`, `{criterion}` 등) 활용

**08_multi_turn.py**
- `input`을 리스트로 제공하여 여러 턴의 대화 히스토리 구성
- 점진적 신뢰 구축 공격 패턴 등 복잡한 시나리오 평가

**09_json.py**
- `json_output`으로 JSON 형식 응답 강제
- Pydantic 모델로 구조화된 데이터 추출 및 검증

<br>

## 2. 실행

### 2.1. UV 설치

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

### 2.2. 환경 변수 설정

1. 환경 변수 지정 (또는 터미널 재실행해도 작동 가능)
```bash
source $HOME/.local/bin/env
```

2. 인식 및 버전 확인
```bash
uv --version
```

### 2.3. 의존성 설치

```bash
uv sync
```

### 2.4. API 키 설정

```bash
# .env 파일 생성
cp env.example .env

# .env 파일 편집하여 OpenAI API 키 입력
# OPENAI_API_KEY=api-key-here
# OPENROUTER_API_KEY=api-key-here
```

> OPENAI API 키 발급: https://platform.openai.com/api-keys

> OPENROUTER API 키 발급: https://openrouter.ai/settings/keys

### 2.5. 기본 실행

```bash
# 예제 번호로 실행 (가장 간단)
uv run python run.py 01
uv run python run.py 02
...
uv run python run.py 09
```

### 2.6. 직접 실행 (고급)

`run.py` 없이 직접 Inspect AI 명령어 사용:

```bash
# 기본 형식
uv run inspect eval <태스크 파일> --model <모델명> [옵션]

# 예시
uv run inspect eval examples/01_hello_world.py \
  --model openai/gpt-4o \
  --log-dir logs/examples/01_hello_world

# 샘플 개수 제한
uv run inspect eval examples/03_multiple_choices.py \
  --model openai/gpt-4o \
  --limit 10 \
  --log-dir logs/examples/03_multiple_choices
```

### 2.7. 도움말 및 목록 확인

```bash
# 간단한 예제 목록
uv run python run.py --list

# 상세한 도움말 (모든 설정 포함)
uv run python run.py --help
```

</br>

## 3. 모델 설정

### 3.1. config.yaml 구조

모든 모델 설정은 `config.yaml` 파일에서 중앙 관리됩니다:

```yaml
# 기본 모델 설정
default_target_model: openai/gpt-4o # 모든 예제에서 사용될 기본 모델
default_options: []

# 예제별 개별 설정
examples:
  "01":
    name: "Hello World"
    description: "기본적인 Hello World 테스트 태스크"
    task: examples/01_hello_world.py
    target_model: openai/gpt-4o  # (override) 이 예제에서 답변 생성시 사용할 모델. 즉, 타겟 모델임. 
    options:
      - --log-dir
      - logs/examples/01_hello_world # log 파일 생성 경로
```

#### OpenAI 모델
```yaml
target_model: openai/gpt-4o          # 최신 GPT-4o
target_model: openai/gpt-4o-mini     # 저렴한 GPT-4o
target_model: openai/gpt-4-turbo     # GPT-4 Turbo
target_model: openai/gpt-3.5-turbo   # GPT-3.5
```

#### Anthropic Claude
```yaml
target_model: anthropic/claude-3-5-sonnet-20241022
target_model: anthropic/claude-3-opus-20240229
```

#### OpenRouter (다양한 모델 지원)
```yaml
target_model: openrouter/google/gemini-2.5-flash
target_model: openrouter/meta-llama/llama-3.1-70b-instruct
```

> OpenRouter 사용 시 환경 변수에 `OPENROUTER_API_KEY` 추가 필요

</br>

## 4. 결과 확인

### 4.1. Inspect View로 결과 확인

실행 결과는 `logs/` 디렉토리에 저장되며, Inspect AI의 웹 인터페이스를 통해 확인할 수 있습니다:

```bash
uv run inspect view
```

실행하면 브라우저가 자동으로 열리거나, http://127.0.0.1:7575 에서 결과를 확인할 수 있습니다.

![Inspect View 화면](./assets/inspect-view-screenshot.png)

**Inspect View 주요 기능:**
- 모든 평가 결과를 시각적으로 확인
- 각 샘플별 상세 결과 (입력, 출력, 채점 결과)
- 성공/실패 통계 및 분석
- 다양한 필터링 및 검색 기능

</br>

## 5. 추가 사용법

### 5.1. 샘플 개수 제한

`config.yaml`에서 `--limit` 옵션 수정:

```yaml
examples:
  "03":
    name: "Multiple Choices"
    options:
      - --limit
      - "10"  # 10개만 테스트
      # - "50"  # 50개로 늘리려면 주석 해제
      # - "100"  # 100개로 늘리려면 주석 해제
```

### 5.2. 로그 디렉토리 변경

로그 저장 위치를 변경하려면:

```yaml
examples:
  "01":
    options:
      - --log-dir
      - logs/my_custom_logs/01_hello_world  # 원하는 경로로 변경
```

### 5.3. 새로운 예제 추가

`config.yaml`에 새 예제 추가:

```yaml
examples:
  "10":
    name: "My Custom Task"
    description: "나만의 커스텀 태스크"
    task: examples/10_my_custom_task.py
    target_model: openai/gpt-4o
    options:
      - --log-dir
      - logs/examples/10_my_custom_task
```

그 후 `examples/10_my_custom_task.py` 파일 생성 후 실행:

```bash
uv run python run.py 10
```

</br>

## 6. 참고 자료

### 공식 문서
- [Inspect AI 공식 문서](https://inspect.ai-safety-institute.org.uk/)
- [Inspect AI GitHub](https://github.com/UKGovernmentBEIS/inspect_ai)
- [Inspect AI 예제 모음](https://github.com/UKGovernmentBEIS/inspect_ai/tree/main/examples)

### 관련 리소스
- [UV 패키지 매니저](https://docs.astral.sh/uv/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [HuggingFace Datasets](https://huggingface.co/datasets)

### 데이터셋
- [HellaSwag](https://rowanzellers.com/hellaswag/) - 상식 추론 벤치마크
- [GSM8K](https://github.com/openai/grade-school-math) - 초등 수학 문제

## 라이선스

이 프로젝트는 학습 목적으로 제공됩니다.  
Inspect AI는 [Apache 2.0 라이선스](https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/LICENSE)를 따릅니다.

