#!/usr/bin/env python3
"""Inspect AI 예제 실행 도우미 스크립트.

YAML 파일을 읽어서 Inspect AI를 실행합니다.

사용법:
    # 기본 사용
    uv run python run.py scripts/01_hello_world.yaml
    
    # 단축 번호로도 실행 가능
    uv run python run.py 01
    
    # 모델 오버라이드
    uv run python run.py scripts/01_hello_world.yaml --model openai/gpt-4o-mini
    uv run python run.py 01 --model gpt-4o-mini
"""

import subprocess
import sys
import yaml
from pathlib import Path

# 단축 번호 매핑
SHORTCUTS = {
    "01": "scripts/01_hello_world.yaml",
    "02": "scripts/02_security_guide.yaml",
    "03": "scripts/03_multiple_choices.yaml",
    "04": "scripts/04_mathematics.yaml",
    "05": "scripts/05_tool_use.yaml",
    "06": "scripts/06_custom_grader_inst.yaml",
    "07": "scripts/07_custom_grader_template.yaml",
    "08": "scripts/08_multi_turn.yaml",
    "09": "scripts/09_json.yaml",
    "10": "scripts/10_all_attack_test.yaml",
}   


def load_config(yaml_path: Path) -> dict:
    """YAML 설정 파일을 로드합니다."""
    if not yaml_path.exists():
        print(f"ERROR: 파일을 찾을 수 없습니다: {yaml_path}")
        sys.exit(1)
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def main():
    if len(sys.argv) < 2:
        print("ERROR: YAML 파일 경로 또는 예제 번호를 지정해주세요.\n")
        print("사용법:")
        print("  uv run python run.py <YAML파일경로>")
        print("  uv run python run.py <예제번호>\n")
        print("예제:")
        print("  uv run python run.py scripts/01_hello_world.yaml")
        print("  uv run python run.py 01\n")
        print("사용 가능한 단축 번호:")
        for num, path in SHORTCUTS.items():
            print(f"  {num} → {path}")
        sys.exit(1)

    # 첫 번째 인자 처리 (YAML 경로 또는 단축 번호)
    arg = sys.argv[1]
    
    # 단축 번호인지 확인
    if arg in SHORTCUTS:
        yaml_path = Path(SHORTCUTS[arg])
        print(f"단축 번호 '{arg}' -> {yaml_path}")
    else:
        yaml_path = Path(arg)
    
    # 설정 로드
    config = load_config(yaml_path)
    
    task_file = config.get('task')
    model = config.get('model')
    options = config.get('options', [])
    
    if not task_file or not model:
        print("ERROR: YAML 파일에 'task'와 'model' 필드가 필요합니다.")
        sys.exit(1)
    
    # 명령줄에서 모델 오버라이드
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model') + 1
        if model_idx < len(sys.argv):
            model = sys.argv[model_idx]
            # openai/ 접두사가 없으면 추가
            if '/' not in model:
                model = f'openai/{model}'
            print(f"모델 오버라이드: {model}")
    
    print(f"실행 중...")
    print(f"Task: {task_file}")
    print(f"Model: {model}")
    if options:
        print(f"Options: {' '.join(options)}")
    print()
    
    # 명령어 구성
    cmd = [
        "uv", "run", "inspect", "eval",
        task_file,
        "--model", model,
    ] + options
    
    # 실행
    try:
        result = subprocess.run(cmd, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: 실행 실패 (exit code: {e.returncode})")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n\n사용자가 중단했습니다.")
        sys.exit(130)


if __name__ == "__main__":
    main()

