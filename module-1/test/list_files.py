from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

for file in current_dir.iterdir():
    if file.is_file() and file.name != current_file:
        content = file.read_text(encoding='utf-8')
        print(f"File: {file.name}")
        print(f"content: {content}")