import os
import subprocess
import cohere
from rich.console import Console
from rich.prompt import Prompt

console = Console()
API_KEY_PATH = "cohere-api-key.txt"

def load_api_key():
    try:
        with open(API_KEY_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        console.print(f"[bold red]API key file not found at {API_KEY_PATH}[/bold red]")
        exit(1)

def init_cohere_client(key):
    return cohere.Client(key)

def build_system_prompt():
    return {
        "role": "SYSTEM",
        "message": (
            "You are a system troubleshooting assistant. The user will describe a problem. "
            "You can ask for more info, run commands using `.execute-command <cmd>`, read files using `.read-file <path>`, or suggest edits using `.edit-file <path>`.\n"
            "Every command you give will be executed if the user confirms. Be specific, and try to diagnose and fix system-level issues."
        )
    }

def run():
    api_key = load_api_key()
    co = init_cohere_client(api_key)
    chat_history = [build_system_prompt()]

    console.print("[bold cyan]Crust Troubleshooter[/bold cyan]")
    console.print("Describe the problem you're facing:")

    while True:
        user_input = Prompt.ask("\n[bold salmon1]❯ Issue[/bold salmon1]")
        if user_input.strip().lower() in ["exit", "quit"]:
            console.print("[bold red]Exiting.[/bold red]")
            break

        chat_history.append({"role": "USER", "message": user_input})
        console.print("[green]Sending to AI...[/green]")
        response = co.chat(message=user_input, chat_history=chat_history)
        console.print(f"[bold cyan]AI Response:[/bold cyan]\n{response.text}")

        lines = response.text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]

            if line.startswith(".execute-command"):
                command = line.replace(".execute-command", "").strip()
                console.print(f"\n[magenta]Run command:[/magenta] [white]{command}[/white]")
                confirm = Prompt.ask("[bold green]OK to run? (yes/no)[/bold green]", default="no")
                if confirm.lower() == "yes":
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    except subprocess.CalledProcessError as e:
                        output = e.output
                    console.print(f"[green]Output:[/green]\n{output}")
                    chat_history.append({
                        "role": "USER",
                        "message": f"The command `{command}` was executed. Output:\n{output}"
                    })
                    # Ask again with new info
                    response = co.chat(message=user_input, chat_history=chat_history)
                    console.print(f"[bold cyan]AI Response (follow-up):[/bold cyan]\n{response.text}")
                    lines = response.text.splitlines()
                    i = 0
                    continue

            elif line.startswith(".read-file"):
                path = line.replace(".read-file", "").strip()
                try:
                    with open(path, "r") as f:
                        contents = f.read()
                    console.print(f"[yellow]Sent contents of {path} to AI[/yellow]")
                    chat_history.append({"role": "USER", "message": f"Contents of `{path}`:\n{contents}"})
                    response = co.chat(message=user_input, chat_history=chat_history)
                    console.print(f"[bold cyan]AI Response (file insight):[/bold cyan]\n{response.text}")
                    lines = response.text.splitlines()
                    i = 0
                    continue
                except Exception as e:
                    console.print(f"[red]Could not read file: {e}[/red]")

            elif line.startswith(".edit-file"):
                path = line.replace(".edit-file", "").strip()
                i += 1
                file_lines = []
                while i < len(lines) and not lines[i].startswith("."):
                    file_lines.append(lines[i])
                    i += 1
                content = "\n".join(file_lines)
                console.print(f"[bold magenta]Edit file {path}?[/bold magenta]")
                confirm = Prompt.ask("[bold green]Confirm overwrite? (yes/no)[/bold green]", default="no")
                if confirm.lower() == "yes":
                    with open(path, "w") as f:
                        f.write(content)
                    console.print(f"[green]File {path} updated.[/green]")
                continue

            i += 1

if __name__ == "__main__":
    run()
