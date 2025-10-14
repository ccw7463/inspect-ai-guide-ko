"""GSM8K 수학 문제 예제: 프롬프트 템플릿과 수치 매칭.

실행 명령어:
    uv run python run.py 04
    
또는:
    uv run inspect eval examples/04_mathematics.py --model openai/gpt-4o --limit 50

예상 흐름:
    GSM8K 데이터셋의 수학 문제를 풀이하고,
    답변을 추출하여 정답과 비교함.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.scorer import match
from inspect_ai.solver import generate, prompt_template

# 답변 형식 지정
MATH_PROMPT_TEMPLATE = """
다음 수학 문제를 단계별로 풀어주세요.
마지막 줄은 반드시 "ANSWER: $ANSWER" 형식으로 작성하세요.

{prompt}

꼭 마지막에 "ANSWER: $ANSWER" 형식으로 답을 작성하세요.

Reasoning:
"""


def record_to_sample(record):
    """GSM8K 레코드를 Inspect AI Sample로 변환."""
    DELIM = "####"
    input_text = record["question"]
    # 답변을 "#### 숫자" 형식으로 분리
    answer = record["answer"].split(DELIM)
    target = answer.pop().strip()  # 마지막 숫자만 정답으로
    reasoning = DELIM.join(answer)  # 풀이 과정

    return Sample(
        input=input_text,
        target=target,  # 정답: "624"
        metadata={"reasoning": reasoning.strip()},  # 풀이 과정 저장
    )


@task
def gsm8k():
    """GSM8K 데이터셋을 사용한 수학 문제 풀이 태스크."""
    return Task(
        dataset=hf_dataset(
            path="gsm8k",
            data_dir="main",
            split="test",
            sample_fields=record_to_sample,  # 데이터 변환
        ),
        solver=[prompt_template(MATH_PROMPT_TEMPLATE), generate()],
        scorer=match(numeric=True),  # 숫자 비교
    )
