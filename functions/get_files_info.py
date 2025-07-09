import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    path = os.path.join(working_directory, directory)
    current_dir = os.path.abspath(path)
    working_dir = os.path.abspath(working_directory)
    
    if not current_dir.startswith(working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    files_list = []
    for item in os.listdir(current_dir):
        item_dir = os.path.join(current_dir, item)
        file_size = os.path.getsize(item_dir)
        is_file = os.path.isfile(item_dir)
        msg = f"{item}: file_size:{file_size} bytes, is_dir={not is_file}"
        files_list.append(msg)

    return "\n".join(files_list)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)