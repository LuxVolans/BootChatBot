import os
import subprocess



schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        # Error Cases:
        if not valid_target_file:
            raise ValueError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file_path):
            raise ValueError(f'"{file_path}" does not exist or is not a regular file')
        if not target_file_path.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        # Run the Python file
        command = ["python", target_file_path] + (args if args else [])
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        


        if result.stdout.strip() == "" and result.stderr.strip() == "":
            return "No output produced"


        output_string = ""
        STDOUT = "" 
        STDERR =  ""
        if result.stdout.strip() != "":
            STDOUT += f"STDOUT: {result.stdout.strip()}"
        if result.stderr.strip() != "":
            STDERR += f"STDERR: {result.stderr.strip()}"
        output_string = f"{STDOUT}\n{STDERR}".strip()


        if result.returncode != 0:
            return f"Process exited with code {result.returncode}\n{output_string}"

        

        return output_string
    except Exception as e:
        return str(f"Error: {e}")

    