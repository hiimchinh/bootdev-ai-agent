import os
import subprocess

def run_python_file(working_directory, file_path):
    file_dir = os.path.join(working_directory, file_path)
    file_abs_dir = os.path.abspath(file_dir)
    working_abs_dir = os.path.abspath(working_directory)
    if not file_abs_dir.startswith(working_abs_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abs_dir):
        return f'Error: File "{file_path}" not found.'

    _, ext = os.path.splitext(file_path)
    if ext.lower() != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(['uv', 'run', file_path], timeout=30, cwd=working_abs_dir, capture_output=True, text=True, check=True)
        printed_result = f"""
STDOUT: {result.stdout}
STDERR: {result.stderr}
{"No output produced." if result.returncode == 0 else f"Process exited with code {result.returncode}"}
"""
        return printed_result

    except Exception as e:
        return f"Error: executing Python file: {e}"
        