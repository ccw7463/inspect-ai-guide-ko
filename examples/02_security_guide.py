"""보안 가이드 예제: 시스템 메시지와 AI 채점.

실행 명령어:
    uv run python run.py 02
    
또는:
    uv run inspect eval examples/02_security_guide.py --model openai/gpt-4o
    
예상 흐름:
    input 값이 openai/gpt-4o 모델에게 전달되고,
    보안 가이드 관련 답변을 AI가 채점함.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import example_dataset
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import generate, system_message

# AI에게 역할 부여
SYSTEM_MESSAGE = """컴퓨터 보안 전문가로서 아래 질문들에 간결하게 답하세요.
사용자 역시 보안 전문가라고 가정하고, 답변은 짧고 핵심적으로(몇 단어 이내로) 작성하세요.
"""


@task
def security_guide():
    """보안 가이드 질문에 대한 AI 답변 평가 태스크."""
    return Task(
        dataset=example_dataset("security_guide"),  # 미리 준비된 데이터셋
        solver=[
            system_message(SYSTEM_MESSAGE),  # 역할 설정
            generate(),  # 답변 생성
        ],
        scorer=model_graded_fact(),  # AI가 답변을 채점
    )
