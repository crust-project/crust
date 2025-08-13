# Configuration Guide

This guide explains how to configure and customize Crust Shell to match your preferences and workflow.

## 📁 Configuration Directory

Crust Shell uses a `.crust` directory for all configuration files. This directory can be located in:
- Your current project directory
- Any parent directory of your current location
- Your home directory

The shell will search upward from your current directory until it finds a `.crust` folder.

## 📝 Configuration Files

### 1. Command Configuration (`cmds.py`)

Located at: `.crust/cmds.py`

This file defines system-wide command preferences and settings.

#### Basic Configuration
```python
# Default text editor
editor = "nvim"  # or "vim", "nano", "code", "subl", etc.

# Package manager commands (if your system uses different commands)
update_system = "sudo pacman -Syu"  # Arch Linux
# update_system = "sudo apt update && sudo apt upgrade"  # Ubuntu/Debian
# update_system = "sudo dnf update"  # Fedora

installpkg = "sudo pacman -S"  # Arch Linux
# installpkg = "sudo apt install"  # Ubuntu/Debian
# installpkg = "sudo dnf install"  # Fedora

removepkg = "sudo pacman -R"  # Arch Linux
# removepkg = "sudo apt remove"  # Ubuntu/Debian
# removepkg = "sudo dnf remove"  # Fedora
```

### 2. Aliases Configuration (`aliases.py`)

Located at: `.crust/aliases.py`

This file defines command aliases and shortcuts.

#### Basic Structure
```python
# Crust Shell Aliases
# Define aliases in the format: alias_name = "command"
import importlib.util
import sys
from pathlib import Path

# Import cmds configuration
current_dir = Path(__file__).parent
cmds_path = current_dir / "cmds.py"
spec = importlib.util.spec_from_file_location("cmds", cmds_path)
cmds = importlib.util.module_from_spec(spec)
sys.modules["cmds"] = cmds
spec.loader.exec_module(cmds)

# File and directory operations
list = "ls"
ll = "ls -l"
la = "ls -la"
cls = "clear"
dir = "ls"
md = "mkdir"
rd = "rmdir"

# File operations
copy = "cp"
move = "mv"
del = "rm"
edit = cmds.editor

# Python aliases
python = "python3"
py = "python3"
pip = "pip3"
```

#### Custom Aliases Examples
```python
# Development shortcuts
serve = "python -m http.server 8000"
venv = "python -m venv"
activate = "source venv/bin/activate"

# Git shortcuts
gst = "git status"
gco = "git checkout"
gcm = "git commit -m"
gps = "git push"
gpl = "git pull"

# Navigation shortcuts
home = "cd ~"
docs = "cd ~/Documents"
projects = "cd ~/Projects"
downloads = "cd ~/Downloads"

# System shortcuts
update = cmds.update_system
install = cmds.installpkg
remove = cmds.removepkg

# Docker shortcuts
dps = "docker ps"
di = "docker images"
dc = "docker-compose"

# Network utilities
myip = "curl ifconfig.me"
ports = "netstat -tuln"
```

#### Dynamic Aliases
```python
# Conditional aliases based on system
import platform
import os

if platform.system() == "Darwin":  # macOS
    open = "open"
    copy_path = "pwd | pbcopy"
elif platform.system() == "Linux":
    open = "xdg-open"
    copy_path = "pwd | xclip -selection clipboard"
elif platform.system() == "Windows":
    open = "start"

# Environment-specific aliases
if os.path.exists("/usr/bin/bat"):
    cat = "bat"  # Use bat instead of cat if available

if os.path.exists("/usr/bin/exa"):
    ls = "exa"   # Use exa instead of ls if available
```

### 3. AI Configuration (`cohere-api-key.txt`)

Located at: `.crust/cohere-api-key.txt`

This file contains your Cohere API key for AI features.

```
your-cohere-api-key-here
```

**Security Notes:**
- Keep this file secure and never commit it to version control
- Add `.crust/cohere-api-key.txt` to your `.gitignore`
- The file should contain only the API key, no extra whitespace or comments

## 🎨 Customization Options

### Prompt Customization

While the prompt format is currently fixed, you can influence what appears by:

1. **Git Repository Names**: The prompt shows the git repository name automatically
2. **Virtual Environment Names**: Activate a virtual environment to see it in the prompt
3. **Directory Structure**: The prompt shows abbreviated paths (~ for home directory)

### Color Scheme

Crust Shell uses the Rich library for coloring. While not directly configurable, you can modify colors by editing the source code in `src/main.py`:

```python
# Current color scheme (in main.py)
git_info = f"[cyan]\\uf1d3 {repo_name} [/][bold green] {branch_name}[/] "
venv_name = f"[pink]{venv_name}"
path_display = f"[cyan][/][bright_cyan]{path}[/]"
prompt_symbol = f"[bold pink1] ＋ [/]"
```

### Custom Commands Integration

You can integrate custom commands by modifying `custom_commands.py`:

```python
import os
import subprocess

def main():
    """Custom startup commands - runs when Crust Shell starts"""
    # Example: Check for updates on startup
    # print("Checking for system updates...")
    
    # Example: Set environment variables
    # os.environ['CUSTOM_VAR'] = 'value'
    
    # Example: Run a command on startup
    # subprocess.run(['notify-send', 'Crust Shell started'], 
    #                capture_output=True)
    pass
```

## 🔧 Advanced Configuration

### Multi-Environment Setup

For different environments (work, personal, different projects):

1. **Project-Specific Configuration**:
   ```bash
   # In each project root
   mkdir .crust
   cp ~/global-crust-config/* .crust/
   # Customize for this project
   ```

2. **Environment Variables in Aliases**:
   ```python
   # In aliases.py
   import os
   
   # Use different configs based on environment
   if os.environ.get('WORK_ENV'):
       git_user = "work-email@company.com"
       editor = "code"
   else:
       git_user = "personal@email.com"
       editor = "nvim"
   
   # Create dynamic aliases
   set_git_user = f"git config user.email {git_user}"
   ```

### Integration with Existing Tools

#### Shell Integration
```python
# In aliases.py - integrate with existing shell functions
source_bashrc = "source ~/.bashrc && exec bash"
reload_zsh = "source ~/.zshrc && exec zsh"
```

#### Editor Integration
```python
# In cmds.py - configure for different editors
editor = "code --wait"  # VS Code with wait flag
# editor = "nvim +startinsert"  # Neovim in insert mode
# editor = "emacs -nw"  # Emacs in terminal
```

#### Package Manager Integration
```python
# In cmds.py - system-specific package managers
import platform

system = platform.system()
if system == "Darwin":
    installpkg = "brew install"
    update_system = "brew update && brew upgrade"
elif system == "Linux":
    # Detect Linux distribution
    with open('/etc/os-release') as f:
        os_info = f.read()
    
    if 'Ubuntu' in os_info or 'Debian' in os_info:
        installpkg = "sudo apt install"
        update_system = "sudo apt update && sudo apt upgrade"
    elif 'Arch' in os_info:
        installpkg = "sudo pacman -S"
        update_system = "sudo pacman -Syu"
    elif 'Fedora' in os_info:
        installpkg = "sudo dnf install"
        update_system = "sudo dnf update"
```

## 📋 Configuration Examples

### Minimal Configuration
```python
# .crust/cmds.py
editor = "nano"

# .crust/aliases.py (minimal imports + basic aliases)
ll = "ls -l"
cls = "clear"
py = "python3"
```

### Power User Configuration
```python
# .crust/cmds.py
editor = "nvim"
update_system = "sudo pacman -Syu"
installpkg = "sudo pacman -S"
removepkg = "sudo pacman -R"
sysinfo_cmd = "neofetch"

# .crust/aliases.py (extensive aliases)
# [Include all the examples from above sections]
```

### Developer Configuration
```python
# .crust/cmds.py
editor = "code"
python_cmd = "python3"

# .crust/aliases.py
# Git workflow
gst = "git status --short"
gco = "git checkout"
gcb = "git checkout -b"
gcm = "git commit -m"
gps = "git push origin HEAD"
gpl = "git pull"
gd = "git diff"
gl = "git log --oneline -10"

# Development servers
serve = "python -m http.server 8000"
serve_php = "php -S localhost:8000"
serve_node = "npx http-server"

# Package management
ni = "npm install"
nid = "npm install --save-dev"
nr = "npm run"
ns = "npm start"
nt = "npm test"

# Python development
venv = "python -m venv venv"
activate = "source venv/bin/activate"
req = "pip freeze > requirements.txt"
install_req = "pip install -r requirements.txt"
```

## 🔄 Reloading Configuration

Changes to configuration files take effect:
- **Immediately** for aliases (used when command is executed)
- **On restart** for cmds.py settings
- **Immediately** for AI API key changes

To reload without restarting:
```bash
# Exit and restart Crust Shell
# Ctrl+C, then python main.py
```

## 🐛 Configuration Troubleshooting

### Common Issues

1. **ImportError in aliases.py**:
   - Check that `cmds.py` exists in the same directory
   - Verify the importlib setup is correct
   - Ensure no syntax errors in configuration files

2. **Aliases not working**:
   - Check syntax in `aliases.py`
   - Verify the alias is defined as a string
   - Ensure no conflicting built-in commands

3. **Commands not found**:
   - Check if the referenced command exists in `cmds.py`
   - Verify the command is properly installed on your system

4. **API key issues**:
   - Ensure the file contains only the key (no extra whitespace)
   - Check file permissions are readable
   - Verify the API key is valid

---

*With your configuration set up, you're ready to make the most of Crust Shell! Check out the [API Reference](api-reference.md) for technical details or the [Contributing Guide](contributing.md) if you want to contribute to the project.*
