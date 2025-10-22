"""
[예제 설명]
    - GSM8K 수학 문제 예제: 프롬프트 템플릿과 수치 매칭
        - 데이터세트 출처 : https://huggingface.co/datasets/openai/gsm8k
    - HuggingFace의 GSM8K 데이터셋을 사용하여 초등학교 수준 수학 문제 풀이
    - prompt_template으로 답변 형식을 지정하고, match scorer로 수치 비교
    - 단계별 풀이 과정을 요구하고 최종 답변에서 숫자만 추출하여 평가
    
[실행 명령어 기본 양식]
    - 형식: uv run inspect eval <예제 파일 경로> 
        - 필수 옵션: --model <평가 대상 모델> 
        - 선택 옵션: --limit <샘플 개수>, --log-dir <로그 저장 경로. 단, logs 폴더 내부로 위치>
    - 예시: uv run inspect eval examples/04_mathematics.py --model openai/gpt-4o --limit 10 --log-dir logs/examples/04_mathematics
    
[실행 명령어 간단한 양식]
    - 형식: uv run python run.py <예제 번호>
    - 예시: uv run python run.py 04
"""

# 라이브러리 가져오기
from inspect_ai import Task, task # Task: 태스크 정의, task: 태스크 실행
from inspect_ai.dataset import Sample, hf_dataset # Sample: 데이터 샘플, hf_dataset: HuggingFace 데이터셋 로더
from inspect_ai.solver import generate, prompt_template # generate: 답변 생성, prompt_template: 프롬프트 템플릿 적용
from inspect_ai.scorer import match # match: 답변 일치 여부 확인 (정규식, 숫자 비교 등)


# 프롬프트 템플릿 정의: 답변 형식 지정
PROMPT_TEMPLATE = """
다음 수학 문제를 단계별로 풀어주세요.

문제 : {prompt}

{output_format}
"""


# 데이터 변환 함수
def record_to_sample(record):
    """GSM8K 레코드를 Inspect AI Sample로 변환하는 함수.
    
    Args:
        record: HuggingFace 데이터셋의 레코드 (dict)
        
    Returns:
        Sample: Inspect AI의 Sample 객체
    """
    DELIMITER = "####"  # GSM8K 데이터셋에서 질문과 답변을 구분하는 구분 문자(delimiter)
    input_text = record["question"]  # 수학 문제 (예: "Janet's ducks lay 16 eggs per day...")
    
    # 답변을 "#### 숫자" 형식으로 분리
    parts = record["answer"].split(DELIMITER)
    reasoning = parts[0].strip()  # 풀이 과정 추출
    target = parts[1].strip()    # 정답 숫자만 추출 (예: "18")
    
    return Sample(
        input=input_text,  # 입력: 수학 문제
        target=target,  # 정답: 숫자 형태 (예: "624")
        metadata={"reasoning": reasoning,
                  "output_format": """꼭 마지막에 "ANSWER: $ANSWER" 형식으로 답을 작성하세요.\n\nReasoning:"""},
    )

# 태스크 정의
@task
def gsm8k():
    return Task(
        dataset=hf_dataset(
            path="gsm8k",  # HuggingFace의 GSM8K 데이터셋
            data_dir="main",  # 데이터 디렉토리
            split="test",  # test 세트 사용 (평가용 데이터)
            sample_fields=record_to_sample,  # 레코드를 Sample로 변환하는 함수 지정
        ),
        solver=[
            # Sample 데이터에 있는 값들이 자동으로 들어감. (input, metadata 등)
            prompt_template(template=PROMPT_TEMPLATE),  # 프롬프트 템플릿 적용 ({prompt}에 sample의 input 값 자동 대입)
            generate()  # 평가 대상 모델에게 입력값을 전달하고, 출력값을 받음
        ],
        scorer=match(numeric=True),  # 숫자 비교 모드 - "ANSWER: 624" 같은 답변에서 숫자만 추출하여 정답과 비교
    )
