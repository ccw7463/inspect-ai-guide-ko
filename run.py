#!/usr/bin/env python3
"""Inspect AI 예제 실행 도우미"""

import subprocess
import sys
import yaml
from pathlib import Path

UNIFIED_CONFIG_PATH = "config.yaml"

def load_unified_config() -> dict:
    config_path = Path(UNIFIED_CONFIG_PATH)
    if not config_path.exists():
        print(f"ERROR: 설정 파일을 찾을 수 없습니다: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_example_config(config: dict, example_num: str) -> dict:
    examples = config.get('examples', {})
    if example_num not in examples:
        print(f"ERROR: 예제 번호 '{example_num}'를 찾을 수 없습니다.")
        print(f"사용 가능한 예제: {', '.join(examples.keys())}")
        sys.exit(1)
    
    example_config = examples[example_num]
    
    if 'target_model' not in example_config:
        example_config['target_model'] = config.get('default_target_model', 'openai/gpt-4o')
    if 'options' not in example_config:
        example_config['options'] = config.get('default_options', [])
    
    return example_config

def show_help(config: dict):
    print("=" * 70)
    print("Inspect AI Guide KO - 도움말")
    print("=" * 70)
    print()
    print("[1] 프로젝트 구조:")
    print("  run.py        - 메인 실행 스크립트")
    print("  config.yaml   - 모든 설정 관리 (모델, 옵션 등)")
    print("  examples/     - 예제 Python 파일들")
    print()
    print("[2] 사용법:")
    print("  uv run python run.py <예제번호>    # 예제 실행")
    print("  uv run python run.py --list        # 간단한 목록")
    print("  uv run python run.py --help        # 이 도움말")
    print()
    print("[3] 설정 변경:")
    print("  모든 설정은 config.yaml 파일에서 관리됩니다.")
    print("  - 모델 변경: 각 예제의 'target_model' 필드 수정")
    print("  - 기본 모델: 'default_target_model' 필드 수정")
    print(f"  - 현재 기본 모델: {config.get('default_target_model', 'openai/gpt-4o')}")
    print()
    print("[4] 사용 가능한 예제:")
    print("-" * 70)
    
    examples = config.get('examples', {})
    for num, example in examples.items():
        name = example.get('name', f'Example {num}')
        description = example.get('description', '')
        task = example.get('task', '')
        target_model = example.get('target_model', config.get('default_target_model', 'openai/gpt-4o'))
        
        print(f"\n{num}. {name}")
        if description:
            print(f"   {description}")
        print(f"   파일: {task}")
        print(f"   모델: {target_model}")
    
    print("\n" + "=" * 70)
    print("[5] 예제:")
    print("  uv run python run.py 01           # Hello World 실행")
    print("  uv run python run.py 03           # Multiple Choices 실행")
    print()


def list_examples(config: dict):
    examples = config.get('examples', {})
    print("사용 가능한 예제:")
    print("=" * 50)
    for num, example in examples.items():
        name = example.get('name', f'Example {num}')
        description = example.get('description', '')
        print(f"{num:2s}. {name}")
        if description:
            print(f"    {description}")
        print()


def main():
    if len(sys.argv) < 2:
        print("ERROR: 예제 번호를 지정해주세요.")
        print("사용법: uv run python run.py <예제번호|--list|--help>")
        sys.exit(1)

    arg = sys.argv[1]
    config = load_unified_config()
    
    if arg == '--help':
        show_help(config)
        sys.exit(0)
    
    if arg == '--list':
        list_examples(config)
        sys.exit(0)
    
    example_config = get_example_config(config, arg)
    
    task_file = example_config.get('task')
    target_model = example_config.get('target_model')
    options = example_config.get('options', [])
    
    print(f"실행: {example_config.get('name', arg)} ({target_model})\n")
    
    cmd = [
        "uv", "run", "python", "-m", "inspect_ai", "eval",
        task_file, "--model", target_model,
    ] + options
    
    try:
        result = subprocess.run(cmd, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: 실행 실패 (exit code: {e.returncode})")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n사용자가 중단했습니다.")
        sys.exit(130)


if __name__ == "__main__":
    main()

