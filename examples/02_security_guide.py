"""
[예제 설명]
    - 보안 가이드 예제: 시스템 메시지와 AI 기반 채점
    - 미리 준비된 example_dataset을 사용하여 보안 관련 질문에 대한 답변 평가
    - system_message로 AI에게 역할을 부여하고, model_graded_fact로 답변의 사실성을 평가
    
[실행 명령어 기본 양식]
    - 형식: uv run inspect eval <예제 파일 경로> 
        - 필수 옵션: --model <평가 대상 모델> 
        - 선택 옵션: --log-dir <로그 저장 경로. 단, logs 폴더 내부로 위치>
    - 예시: uv run inspect eval examples/02_security_guide.py --model openai/gpt-4o --log-dir logs/examples/02_security_guide
    
[실행 명령어 간단한 양식]
    - 형식: uv run python run.py <예제 번호>
    - 예시: uv run python run.py 02
"""

# 라이브러리 가져오기
from inspect_ai import Task, task # Task: 태스크 정의, task: 태스크 실행
from inspect_ai.dataset import example_dataset # example_dataset: Inspect AI에서 제공하는 미리 준비된 데이터셋
from inspect_ai.solver import generate, system_message # generate: 답변 생성, system_message: 시스템 메시지 설정
from inspect_ai.scorer import model_graded_fact # model_graded_fact: AI가 답변의 사실성을 평가

# 시스템 메시지 정의: AI에게 역할 부여
SYSTEM_MESSAGE = """컴퓨터 보안 전문가로서 아래 질문들에 간결하게 답하세요.
사용자 역시 보안 전문가라고 가정하고, 답변은 짧고 핵심적으로(몇 단어 이내로) 작성하세요.
"""


# 태스크 정의
@task
def security_guide():
    return Task(
        dataset=example_dataset("security_guide"),  # Inspect AI에서 제공하는 미리 준비된 보안 가이드 데이터셋 사용
        solver=[
            system_message(SYSTEM_MESSAGE),  # AI에게 보안 전문가 역할 부여
            generate(),  # 평가 대상 모델에게 입력값을 전달하고, 출력값을 받음
        ],
        scorer=model_graded_fact(),  # AI(평가 모델)가 답변의 사실성을 평가 (사실에 기반한 답변인지 확인)
    )
