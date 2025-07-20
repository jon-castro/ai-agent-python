import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))

        if not target_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        result = []
        for name in os.listdir(target_path):
            item_path = os.path.join(target_path, name)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
            except Exception as e:
                size = 0
            result.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result)

    except Exception as e:
        return f"Error: {str(e)}"


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
