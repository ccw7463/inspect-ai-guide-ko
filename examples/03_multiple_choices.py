"""HellaSwag 예제: 객관식 문제와 HuggingFace 데이터셋.

실행 명령어:
    uv run python run.py 03
    
또는:
    uv run inspect eval examples/03_multiple_choices.py --model openai/gpt-4o --limit 50

예상 흐름:
    HuggingFace의 HellaSwag 데이터셋을 로드하여,
    가장 그럴듯한 이야기 전개를 선택하는 태스크를 수행함.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice, system_message


def record_to_sample(record):
    """HuggingFace 레코드를 Inspect AI Sample로 변환."""
    return Sample(
        input=record["ctx"],  # 질문
        target=chr(ord("A") + int(record["label"])),  # 정답을 A, B, C로 변환 -> 보기들 중 하나를 선택하도록
        choices=record["endings"],  # 보기들
    )


@task
def hellaswag():
    """HellaSwag 데이터셋을 사용한 객관식 문제 태스크."""
    dataset = hf_dataset(
        path="hellaswag",  # HuggingFace에서 데이터 가져오기
        split="validation", # validation 데이터셋을 사용함
        sample_fields=record_to_sample,
        trust=True,
    )

    return Task(
        dataset=dataset,
        solver=[
            system_message("가장 그럴듯한 이야기 전개를 고르세요."), # 시스템 메시지 설정
            multiple_choice(),  # 객관식 전용 solver -> 보기들 중 하나를 선택하는 것
        ],
        scorer=choice(),  # 객관식 전용 채점 -> 보기들 중 하나를 선택하는 것
    )
