import base
import os
import time
import subprocess
import custom_commands 
import sys
import cohere
import troubleshooting
import capk
import lang

# Try to run any custom startup commands
try:
    custom_commands.main()
except Exception as e:
    # Print error if custom commands fail
    base.console.print(f" Error executing custom commands: {e}", style="bold red")

# Main interactive shell loop
while True:
    try:
        # I am sorry
        # for now removed, causing problems with dirs
        """with open("./venv_prompt.txt") as f:
            show_venv = f.read()
            if show_venv.strip().lower() != "yes":
                show_venv = False
        try:
            del show_venv
            show_venv = False
        except NameError:
            show_venv = True"""
        
        # Get current virtual environment name (if any)
        venv_path = os.environ.get('VIRTUAL_ENV') or sys.prefix
        venv_name = " " + os.path.basename(venv_path.rstrip(os.sep)) if venv_path else None
        if venv_name == " usr":
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
                git_info = f"[cyan]\uf1d3 {repo_name} [/][bold green] {branch_name}[/] "
        except Exception:
            # Ignore git errors
            pass
        
        username = os.getlogin()
        path = os.getcwd().replace("/home/" + username, " ~")

        # Print prompt with git, venv, and current directory info. string for now for the commented code above
        if "show_venv and venv_name": 
            venv_name = f"[pink]{venv_name}"
        else:
            venv_name = ""
        base.console.print(
            f"{git_info}"
            f"[pink1]{venv_name}[/] "
            f"[cyan][/][bright_cyan]{path}[/]"
            f"[bold pink1] ＋ [/]",
            end=""
        )

        # Read user input
        prompt = input()

        # Handle 'ls' command: show directory listing in a table
        if prompt == "ls" or prompt == "ls -l" or prompt == "ls -la":
            table = base.Table(title="󰉋 Directory Listing", show_lines=True)
            table.add_column("󰈔 Name", style="cyan")
            table.add_column("󰊢 Type", style="magenta")
            table.add_column("󰍛 Size", style="green")
            table.add_column("󰥔 Modified", style="yellow")
            try:
                for entry in os.listdir('.'):
                    entry_path = os.path.join('.', entry)
                    if os.path.isdir(entry_path):
                        entry_type = " Directory"
                        size = "-"
                    else:
                        entry_type = " File"
                        size = f"{os.path.getsize(entry_path)} bytes"
                    modified_time = time.ctime(os.path.getmtime(entry_path))
                    table.add_row(f"{entry}", entry_type, size, modified_time)
                base.console.print(table)
            except Exception as e:
                base.console.print(f"󰅚 Error listing directory: {e}", style="bold red")
        elif prompt == "disk usage" or prompt == "df -h":
            try:
                output = subprocess.check_output(["df", "-h"], text=True)
                lines = output.strip().split("\n")
                headers = lines[0].split()
                table = base.Table(title="💾 Disk Usage", show_lines=True)
                for h in headers:
                    table.add_column(h, style="cyan")

                for line in lines[1:]:
                    table.add_row(*line.split())

                base.console.print(table)
            except Exception as e:
                base.console.print(f"[red]Error running df: {e}[/red]")

        elif prompt.startswith("capk"):
            package = prompt.replace("capk ", "")
            capk.search(package)

        elif prompt == "lsusb":
            try:
                output = subprocess.check_output(["lsusb"], text=True)
                lines = output.strip().split("\n")

                # if theres a table existing, remove it
                try:
                    del table
                except NameError:
                    pass

                table = base.Table(title=" USB Devices", show_lines=True)
                table.add_column("Bus", style="cyan")
                table.add_column("Device", style="green")
                table.add_column("ID", style="magenta")
                table.add_column("Description", style="yellow")

                for line in lines:
                    parts = line.split()
                    bus = parts[1]
                    device = parts[3].strip(":")
                    usb_id = parts[5]
                    description = " ".join(parts[6:])
                    table.add_row(bus, device, usb_id, description)

                base.console.print(table)
            except FileNotFoundError:
                base.console.print("󰍉 'lsusb' not found.", style="bold red")
            except Exception as e:
                base.console.print(f"󰅚 Error running lsusb: {e}", style="bold red")
        elif prompt == "troubleshooting":
            print("Connecting...")
            troubleshooting.run()
        elif prompt == "about":
            from rich.table import Table as RichTable
            plus_lines = [" + ", "+++", " + "]
            about_lines = [
                "[bold salmon1]Crust Shell[/]",
                "Author: Juraj Kollár (mostypc123)",
                "Version: dev"
            ]
            table = RichTable(show_header=False, box=None, pad_edge=False)
            table.add_column(justify="left", style="bold salmon1")  # icon column
            table.add_column(justify="left", style="bold white")    # info column
            for plus, about in zip(plus_lines, about_lines):
                table.add_row(plus, about)
            base.console.print(table)
            continue

        elif prompt.startswith("cd"):
            entered_dir = prompt.replace("cd ", "")
            os.chdir(entered_dir)
        
        elif prompt.startswith(".question"):
            with open("cohere-api-key.txt", "r") as f:
                key = f.read().strip()

            try:
                test = no_cohere
                del test
            except Exception:
                co = None

            if co:
                no_cohere = False
                base.console.print("[yellow]Skipping creation of the Cohere client.[/yellow]")
            else:
                no_cohere = True
                base.console.print("[bold green]Creating a new Cohere client...[/bold green]")
                co = cohere.Client(key)

                base.console.print("[cyan]Giving the output of neofetch to the AI, so it can understand the system.[/cyan]")
                os_info = __import__('subprocess').check_output('neofetch --stdout', shell=True, text=True)

                base.console.print("[cyan]Giving extra info to the AI...[/cyan]")
                chat_history = [{
                    "role": "SYSTEM",
                    "message": (
                        "you are an integrated assistant in a linux shell called crust. if .question gets in to the prompt, its normal, that is the command to ask a question."
                        "to execute commands, write `.execute-command` before it. do not put the ` there. after every `.execute-command`,create a new line and put this in it:\n"
                        ":The assistant is sometimes buggy when executing, and may hallucinate from the knowledge base.:\n"
                        "If the user gives the output of a command you asked to execute, do not ask to execute it again. Instead, reason from the output they gave."
                        "prefer executing it like this instead of telling the user to execute it themselves. you ARE ABLE TO EXECUTE COMMANDS. "
                        "IF YOU ARE ASKED FOR A COMMAND, EXECUTE IT LIKE THAT. YOU CAN EXECUTE COMMANDS. JUST EXECUTE WITHOUT ANYTHING SAID. "
                        "YOU AREN'T A TEXT-BASED AI ONLY, THE SHELL IS INTEGRATED WITH YOU. DO NOT PRETEND TO EXECUTE. "
                        "THE COMMANDS WILL GET EXECUTED IN THE BACKEND AFTER SCANNING FOR EXECUTING COMMANDS BY YOU.\n\n"

                        "To modify files, use `.edit-file /path/to/file` followed by the full content you want to write to the file. "
                        "Do NOT describe the change in words — just show the updated contents. "
                        "Only start the new content after the `.edit-file` line. You can edit scripts, config files, or create new ones. "
                        "Assume full permission to overwrite them, unless told otherwise.\n\n"

                        "To view a file, use `.read-file /path/to/file`. This will return the file contents to you in the next message. "
                        "Only request one file per `.read-file` line.\n\n"

                        "The text you say is viewed as plain text, so don't use markdown or any similar formatting. "
                        "THIS MESSAGE IS NOT SENT BY THE USER.\n\n"

                        "For showing accurate information, here is a run of neofetch. If it shows an error, ignore it. Do not use it while asking for execution of neofetch, use only when asking for system specs and similar:\n"
                        + os_info
                    )
                }]

            base.console.print("[blue]Processing prompt (1/2)...[/blue]")
            chat_history.append({"role": "USER", "message": prompt})

            base.console.print("[blue]Processing prompt (2/2)...[/blue]")
            response = co.chat(message=prompt, chat_history=chat_history)
            lines = response.text.splitlines()

            base.console.print("[bold cyan]AI Response:[/bold cyan]\n" + response.text)
            base.console.print("[green on white]Scanning for commands, file edits, and reads...[/green on white]")

            i = 0
            while i < len(lines):
                line = lines[i]

                if line.startswith(".execute-command"):
                    command = line.replace(".execute-command", "").strip()
                    base.console.print("[magenta on white]Found an execution of a command in the response[/magenta on white]")
                    base.console.print(f"[bold green]OK if I execute this command? yes/no:[/bold green] [white]{command}[/white]")
                    exec_it = input()
                    if exec_it == "yes":
                        try:
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                        except subprocess.CalledProcessError as e:
                            output = e.output

                        base.console.print(f"[green]Command output:[/green]\n{output}")
                        chat_history.append({
                            "role": "USER",
                            "message": f"The command `{command}` has already been executed. Here's the result:\n{output}"
                        })
                        base.console.print("[yellow]Sending command output back to AI...[/yellow]")

                        response = co.chat(message=prompt, chat_history=chat_history)
                        base.console.print("[bold cyan]New AI Response:[/bold cyan]\n" + response.text)
                    i += 1
                    continue

                elif line.startswith(".edit-file"):
                    filepath = line.replace(".edit-file", "").strip()
                    base.console.print(f"[magenta on white]Found a file edit request for:[/magenta on white] [bold]{filepath}[/bold]")
                    i += 1
                    file_lines = []

                    while i < len(lines) and not lines[i].startswith("."):
                        file_lines.append(lines[i])
                        i += 1

                    file_content = "\n".join(file_lines)
                    base.console.print(f"[bold green]OK if I overwrite this file? yes/no:[/bold green] [white]{filepath}[/white]")
                    exec_it = input()
                    if exec_it == "yes":
                        with open(filepath, "w") as f:
                            f.write(file_content)
                        base.console.print(f"[green]File {filepath} written.[/green]")
                    continue

                elif line.startswith(".read-file"):
                    filepath = line.replace(".read-file", "").strip()
                    base.console.print(f"[bold cyan]AI requested to read file:[/bold cyan] {filepath}")
                    try:
                        with open(filepath, "r") as f:
                            file_contents = f.read()
                        base.console.print(f"[green]Sending file contents back to AI...[/green]")

                        chat_history.append({"role": "USER", "message": f"Contents of `{filepath}`:\n{file_contents}"})
                        base.console.print("[yellow]Re-querying AI with file contents...[/yellow]")
                        response = co.chat(message=prompt, chat_history=chat_history)
                        base.console.print("[bold cyan]New AI Response:[/bold cyan]\n" + response.text)
                        # optionally: re-run the parsing loop again here
                        break  # or continue outer logic

                    except Exception as e:
                        base.console.print(f"[red]Could not read file {filepath}: {e}[/red]")
                    i += 1
                    continue

                i += 1


        # For all other commands, run them in the shell
        if prompt in ["about", "lsusb", "ls", "ls -l", "ls -la", "disk usage", "df -h"] or prompt.startswith(".question") or prompt.startswith("capk "):
            continue
        else:
            try:
                language = lang.detect(prompt)
                allowed = {"python3", "bash", "zsh", "fish"}
                if language not in allowed:
                    language = "bash"
                cmd = [language, "-c", prompt]
                subprocess.run(cmd)
            except KeyboardInterrupt:
                base.console.print("\n KeyboardInterrupt detected during command. Returning to prompt...\n", style="bold red")

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit the shell
        base.console.print("\n KeyboardInterrupt detected. Exiting...\n", style="bold red")
        base.console.file.flush()
        time.sleep(0.1) # Allow time for console to flush
        break
    except Exception as e:
        # Catch-all for unexpected errors
        base.console.print(f"󰅚 An error occurred: {e}", style="bold red")
        continue
