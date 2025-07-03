import os

def write_file(working_directory, file_path, content):
    file_dir = os.path.join(working_directory, file_path)
    if not file_dir.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(file_dir, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing the file to {file_dir} failed, details: {e}'
    
