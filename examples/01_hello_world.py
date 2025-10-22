"""
[예제 설명]
    - 기본적인 Hello World 테스트

[실행 명령어 기본 양식]
    - 형식: uv run inspect eval <예제 파일 경로> 
        - 필수 옵션: --model <평가 대상 모델> 
        - 선택 옵션: --log-dir <로그 저장 경로. 단, logs 폴더 내부로 위치>
    - 예시: uv run inspect eval examples/01_hello_world.py --model openai/gpt-4o --log-dir logs/examples/01_hello_world
    
[실행 명령어 간단한 양식]
    - 형식: uv run python run.py <예제 번호>
    - 예시: uv run python run.py 01
"""

# 라이브러리 가져오기
from inspect_ai import Task, task # Task: 태스크 정의, task: 태스크 실행
from inspect_ai.dataset import Sample # Sample: 입력값과 정답을 저장하는 데이터셋
from inspect_ai.solver import generate # generate() 함수는 평가 대상 모델에게 입력값을 전달하고, 출력값을 받음
from inspect_ai.scorer import exact # exact() 함수는 출력값이 정답(target)과 정확히 일치하는지 확인함

# 태스크 정의
@task
def hello_world():
    return Task(
        dataset=[
            Sample(
                input="Just reply with Hello World", # 입력값
                target="Hello World", # 정답
            )
        ],
        solver=[generate()], # generate() 함수는 평가 대상 모델에게 입력값을 전달하고, 출력값을 받음
        scorer=exact(), # exact() 함수는 출력값이 정답(target)과 정확히 일치하는지 확인함
    )
