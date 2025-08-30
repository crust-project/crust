import os

def python(project_name):
    """
    Create a basic Python project skeleton in the current working directory.
    
    This function scaffolds a minimal Python project: it creates requirements.txt (empty), writes a pyproject.toml skeleton (the file contains a literal name field 'name = "{project_name}"' and other template entries), writes README.md containing the provided project_name, creates a src/ package with __init__.py (setting __version__ = "0.1.0") and an empty main.py, creates a docs/ directory, initializes a Git repository (runs `git init`), and writes a .gitignore that ignores .vscode, .idea, and Python cache patterns. Filesystem operations are performed directly and sequentially; there is no return value and no internal error handling—exceptions raised by file or OS operations will propagate.
     
    Parameters:
        project_name (str): Project name written into README.md. Note that the pyproject.toml created by this function contains the literal placeholder "{project_name}" and is not programmatically substituted.
    """
    print("Making a Python project structure...")

    print("Creating requirements.txt")
    with open("requirements.txt", "w") as f:
        f.write("")

    print("Creating a pyproject.toml file skeleton..")
    with open("pyproject.toml", "w") as f:
        f.write("""
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
license = {{ file = "LICENSE" }}
authors = [
  {{ name = "" }}
]
requires-python = ">=3.8"
dependencies = []
        """)

    print("Creating a README.md skeleton..")
    with open("README.md", "w") as f:
        f.write(f"{project_name}")

    print("Creating the src directory...")
    os.mkdir("src")

    print("Creating skeleton files in the src directory..")
    os.chdir("src")

    with open("__init__.py", "w") as f:
        f.write('__version__ = "0.1.0"')

    with open("main.py", "w") as f:
        f.write("")

    os.chdir("..")

    print("Creating a docs/ directory...")
    os.mkdir("docs")

    print("Creating a git repo...")
    os.system("git init")

    with open(".gitignore", "w") as f:
        f.write(".vscode\n.idea\n*__pycache__*")
