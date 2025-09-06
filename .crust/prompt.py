import os
import sys
import subprocess
import base

def main():
    """
    Edit this function to match what you want the prompt to look like
    """
    # Get current virtual environment name (if any)
    venv_path = os.environ.get('VIRTUAL_ENV') or sys.prefix
    venv_name = " " + os.path.basename(venv_path.rstrip(os.sep)) if venv_path else None
    if venv_name == " usr":
        venv_name = ""

    git_info = ""
    try:
        # Check if in a git repo and get repo/branch info
        git_dir = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
        if git_dir.returncode == 0:
            repo_path = git_dir.stdout.strip()
            repo_name = os.path.basename(repo_path)
            # Get branch name
            branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            branch_name = branch.stdout.strip() if branch.returncode == 0 else '?'
            git_info = f"[cyan]\uf1d3 {repo_name} [/][bold green] {branch_name}[/] "
    except Exception:
        # Ignore git errors
        pass
    
    username = os.getlogin()
    path = os.getcwd().replace("/home/" + username, " ~")

    # Print prompt with git, venv, and current directory info
    show_venv = True  # You can change this to False if you don't want to show venv
    if show_venv and venv_name: 
        venv_name = f"[pink]{venv_name}[/]"
    else:
        venv_name = ""
    
    base.console.print(
        f"{git_info}"
        f"{venv_name}"
        f"[cyan][/][bright_cyan]{path}[/]"
        f"[bold pink1] ＋ [/]",
        end=""
    )
