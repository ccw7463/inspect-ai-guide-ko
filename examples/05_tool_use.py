"""도구 사용 예제: 도구 사용 권한 주고, 1 + 1을 계산하게 함.

실행 명령어:
    uv run python run.py 05 
    
또는:
    uv run inspect eval examples/05_tool_use.py --model openai/gpt-4o

예상 흐름:
    AI에게 add() 함수 사용 권한 주고,
    1 + 1을 계산하게 함.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate, use_tools, prompt_template
from inspect_ai.tool import tool

# 프롬프트 템플릿 정의
MATH_PROMPT_TEMPLATE = """
당신은 수학 선생님입니다. 사용자가 수학 문제 풀이를 요청하면 무조건 정답 숫자만 작성하세요.

사용자 요청 : {prompt}
"""


# 도구 정의
@tool
def add():
    async def execute(x: int, y: int):
        """
        두 숫자를 더합니다.

        Args:
            x: 첫 번째 숫자
            y: 두 번째 숫자

        Returns:
            두 숫자의 합
        """
        return x + y
    return execute

@task
def addition_problem():
    return Task(
        dataset=[Sample(
            input="1 + 1은 얼마인가요?",
            target=["2", "2.0"]
        )],
        solver=[
            prompt_template(MATH_PROMPT_TEMPLATE), # input 값이 prompt 변수로 들어감
            use_tools(add()),  # AI에게 add() 함수 사용 권한 주기
            generate()
        ],
        scorer=match(numeric=True),
    )