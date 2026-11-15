import os
from config import MAX_CHARACTERS



schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The content of the file, truncated to a maximum of 10000 characters",
                },
            },
            "required": ["file_path"],
        },
    },
}



def get_file_content(working_directory: str, file_path: str) -> str:


    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        # Error Cases:
        if not valid_target_file:
            raise ValueError(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file_path):
            raise ValueError(f'"File not found or is not a regular file: {file_path}"')



        with open(target_file_path, 'r') as file:
            content = file.read(MAX_CHARACTERS)
            if file.read(MAX_CHARACTERS) != '':
                content += f'[... File "{file_path}" truncated at {MAX_CHARACTERS} characters.]'
            return content
    except Exception as e:
        return str(f"Error: {e}")