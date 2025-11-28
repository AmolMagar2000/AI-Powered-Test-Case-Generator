# utils/code_utils.py
import re

def parse_generated_code(code_text):
    files = {}
    current_file = None
    buffer = []

    for line in code_text.splitlines():
        m = re.match(r"// FILE: (.+)", line)
        if m:
            if current_file and buffer:
                files[current_file] = "\n".join(buffer).strip()
            current_file = m.group(1).strip()
            buffer = []
        else:
            if current_file:
                buffer.append(line)
    if current_file and buffer:
        files[current_file] = "\n".join(buffer).strip()
    return files
