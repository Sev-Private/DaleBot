import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print its output."""
    try:
        print(f"Running: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main(target):
    """Run formatting tools on the target file or directory."""
    if not os.path.exists(target):
        print(f"Error: Target '{target}' does not exist.")
        sys.exit(1)

    tools = [
        ["black", target],
        ["isort", target],
        ["autoflake", "--in-place", "--remove-unused-variables", target],
    ]

    for tool in tools:
        run_command(tool)

    print(f"Linting and formatting completed for {target}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_and_format.py <file_or_directory>")
        sys.exit(1)

    main(sys.argv[1])
