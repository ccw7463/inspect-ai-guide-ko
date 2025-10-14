"""Inspect AI 기본 예제: Hello World.

실행 명령어:
    uv run python run.py 01
    
또는:
    uv run inspect eval examples/01_hello_world.py --model openai/gpt-4o

예상 흐름:
    input 값이 openai/gpt-4o 모델에게 전달되고,
    target 값이 "Hello World"인지 확인하게 됨.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import generate


@task
def hello_world():
    """기본적인 Hello World 테스트 태스크."""
    return Task(
        dataset=[
            Sample(
                input="Just reply with Hello World",
                target="Hello World",
            )
        ],
        solver=[generate()], # generate() 함수는 모델에게 입력값을 전달하고, 출력값을 받음
        scorer=exact(), # exact() 함수는 출력값이 정답(target)과 정확히 일치하는지 확인함
    )
