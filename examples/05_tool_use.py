"""
[예제 설명]
    - 도구 사용 예제: AI에게 함수 실행 권한 부여
    - @tool 데코레이터로 Python 함수를 AI가 호출 가능한 도구로 변환
    - use_tools로 AI에게 도구 사용 권한을 부여하여 문제 해결
    - AI가 자율적으로 도구를 선택하고 호출하여 정확한 답변을 생성
    
[실행 명령어 기본 양식]
    - 형식: uv run inspect eval <예제 파일 경로> 
        - 필수 옵션: --model <평가 대상 모델> 
        - 선택 옵션: --log-dir <로그 저장 경로. 단, logs 폴더 내부로 위치>
    - 예시: uv run inspect eval examples/05_tool_use.py --model openai/gpt-4o --log-dir logs/examples/05_tool_use
    
[실행 명령어 간단한 양식]
    - 형식: uv run python run.py <예제 번호>
    - 예시: uv run python run.py 05
"""

# 라이브러리 가져오기
from inspect_ai import Task, task # Task: 태스크 정의, task: 태스크 실행
from inspect_ai.dataset import Sample # Sample: 입력값과 정답을 저장하는 데이터셋
from inspect_ai.solver import generate, use_tools, prompt_template # generate: 답변 생성, use_tools: 도구 사용 권한 부여, prompt_template: 프롬프트 템플릿 적용
from inspect_ai.scorer import match # match: 답변 일치 여부 확인
from inspect_ai.tool import tool # tool: 함수를 AI가 사용 가능한 도구로 변환하는 데코레이터

# 프롬프트 템플릿 정의: 답변 형식 지정
PROMPT_TEMPLATE = """
당신은 수학 선생님입니다. 사용자가 수학 문제 풀이를 요청하면 무조건 정답 숫자만 작성하세요.

사용자 요청 : {prompt}
"""


# 도구 정의: AI가 사용할 수 있는 함수 생성
@tool
def add():
    """덧셈 도구를 생성하는 함수."""
    async def execute(x: int, y: int):
        """
        두 숫자를 더하는 함수.
        AI가 이 함수를 호출할 때 사용할 수 있는 docstring 정보.

        Args:
            x: 첫 번째 숫자
            y: 두 번째 숫자

        Returns:
            두 숫자의 합
        """
        return x + y  # 실제 덧셈 연산 수행
    return execute


# 태스크 정의
@task
def addition_problem():
    return Task(
        dataset=[
            Sample(
                input="1 + 1은 얼마인가요?",  # 입력: 덧셈 문제
                target=["2", "2.0"]  # 정답: 여러 형식 허용 (문자열 "2" 또는 "2.0")
            )
        ],
        solver=[
            prompt_template(template=PROMPT_TEMPLATE),  # 프롬프트 템플릿 적용 (sample의 input 값이 {prompt} 변수로 자동 대입됨)
            use_tools(add()),  # AI에게 add() 함수 사용 권한 부여 - AI가 필요 시 이 함수를 호출할 수 있음
            generate()  # AI가 도구를 활용하여 답변 생성
        ],
        scorer=match(numeric=True),  # 숫자 비교 모드 - 문자열 "2"와 "2.0"을 동일하게 평가
    )