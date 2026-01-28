import subprocess
import tempfile
import os

def run_code(code: str, input_data: str, timeout=2):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        file_path = f.name

    try:
        result = subprocess.run(
            ["python", file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout.strip()
    except subprocess.TimeoutExpired:
        output = "TIMEOUT"
    finally:
        os.remove(file_path)

    return output
