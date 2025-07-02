import os

def get_file_content(working_directory, file_path):
    file_full_path = os.path.join(working_directory, file_path)
    file_dir = os.path.abspath(file_full_path)
    working_dir = os.path.abspath(working_directory)
    if not file_dir.startswith(working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_dir):
        return f'Error: File not found or is not a regular file "{file_path}"'

    try:
        MAX_CHARS = 10000
        with open(file_dir, 'r') as f:
            file_content = f.read(MAX_CHARS)
            next_char = f.read(1)
            if next_char:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'

            return file_content
    except Exception as err:
        return f"Error: Caught exception reading the content string: {err}"