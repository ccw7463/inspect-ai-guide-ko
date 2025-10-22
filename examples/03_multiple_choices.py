"""
[예제 설명]
    - HellaSwag 예제: 객관식 문제와 HuggingFace 데이터셋
        - 데이터세트 출처 : https://huggingface.co/datasets/Rowan/hellaswag
    - HuggingFace의 HellaSwag 데이터셋을 사용하여 이야기 전개 예측
    - 주어진 문맥에서 가장 그럴듯한 다음 이야기를 선택하는 상식 추론 평가
    - multiple_choice solver와 choice scorer를 사용하여 객관식 문제 처리
    
[실행 명령어 기본 양식]
    - 형식: uv run inspect eval <예제 파일 경로> 
        - 필수 옵션: --model <평가 대상 모델> 
        - 선택 옵션: --limit <샘플 개수>, --log-dir <로그 저장 경로. 단, logs 폴더 내부로 위치>
    - 예시: uv run inspect eval examples/03_multiple_choices.py --model openai/gpt-4o --limit 10 --log-dir logs/examples/03_multiple_choices
    
[실행 명령어 간단한 양식]
    - 형식: uv run python run.py <예제 번호>
    - 예시: uv run python run.py 03
"""

# 라이브러리 가져오기
from inspect_ai import Task, task # Task: 태스크 정의, task: 태스크 실행
from inspect_ai.dataset import Sample, hf_dataset # Sample: 데이터 샘플, hf_dataset: HuggingFace 데이터셋 로더
from inspect_ai.solver import multiple_choice, system_message # multiple_choice: 객관식 solver, system_message: 시스템 메시지 설정
from inspect_ai.scorer import choice # choice: 객관식 문제 채점기


# 데이터 변환 함수
def record_to_sample(record):
    """HuggingFace 레코드를 Inspect AI Sample로 변환하는 함수.
    
    Args:
        record: HuggingFace 데이터셋의 레코드 (dict)
        
    Returns:
        Sample: Inspect AI의 Sample 객체
    """
    return Sample(
        input=record["ctx"],  # 이야기의 시작 문맥 (예: "사람이 자전거를 타고 있다...")
        target=chr(ord("A") + int(record["label"])),  # 정답값을 숫자(0,1,2,3)에서 문자(A,B,C,D)로 변환
                                                      # ord : 문자의 아스키 코드 값을 반환 (예: "A" -> 65, "B" -> 66, "C" -> 67, "D" -> 68)
        choices=record["endings"],  # 선택 가능한 보기 4가지 목록 (이야기의 가능한 전개들)
    )

# 시스템 메시지 정의
SYSTEM_MESSAGE = "가장 그럴듯한 이야기 전개를 고르세요."

# 태스크 정의
@task
def hellaswag():
    dataset = hf_dataset(
        path="hellaswag",  # HuggingFace 데이터셋 이름
        split="validation", # validation 세트 사용 (학습용이 아닌 검증용 데이터)
        sample_fields=record_to_sample,  # 레코드를 Sample로 변환하는 함수 지정
        trust=True,  # 데이터셋 로드 시 신뢰 설정
    )

    return Task(
        dataset=dataset,  # 로드한 데이터셋 사용
        solver=[
            system_message(SYSTEM_MESSAGE), # AI에게 작업 지시
            multiple_choice(),  # 객관식 문제 전용 solver - 보기들을 A, B, C, D 형식으로 제시하고 선택하게 함
        ],
        scorer=choice(),  # 객관식 문제 전용 채점기 - AI가 선택한 답(A, B, C, D)이 정답과 일치하는지 확인
    )
