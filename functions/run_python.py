import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_path.startswith(base_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Build the command
        cmd = ["python", target_path] + args

        # Run the process
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=base_path,
            timeout=30
        )

        output = []
        if result.stdout:
            output.append("STDOUT:\n" + result.stdout)
        if result.stderr:
            output.append("STDERR:\n" + result.stderr)
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not output:
            return "No output produced."

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
