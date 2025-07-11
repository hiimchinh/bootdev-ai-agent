import os
from google.genai import types

def write_file(directory, file_path, content):
    file_dir = os.path.join(directory, file_path)
    if not file_dir.startswith(directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(file_dir, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing the file to {file_dir} failed, details: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the file in the specified directory, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to the file to write content, relative to the working directory"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to write content to, inside the specified directory"
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description="The content to write the the file"
            )
        }
    )
)