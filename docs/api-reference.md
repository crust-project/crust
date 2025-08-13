# API Reference

This document provides technical reference information for Crust Shell's modules, functions, and internal APIs.

## 📁 Project Structure

```
crust/
├── src/                    # Main source code
│   ├── main.py            # Main shell loop and interface
│   ├── base.py            # Core console and UI components
│   ├── config_find.py     # Configuration directory discovery
│   ├── capk.py            # Package availability checker
│   ├── troubleshooting.py # AI-powered troubleshooting
│   └── custom_commands.py # Custom startup commands
├── .crust/                # Configuration directory
│   ├── aliases.py         # Command aliases configuration
│   ├── cmds.py           # System commands configuration
│   └── cohere-api-key.txt # AI API key
└── docs/                  # Documentation
```

## 🔧 Core Modules

### main.py

The main module contains the interactive shell loop and command processing logic.

#### Key Functions

**Shell Loop**
```python
while True:
    # Main interactive loop
    # Handles prompt display, input processing, and command execution
```

**Prompt Generation**
- Git repository detection and branch information
- Virtual environment detection
- Current directory display with home abbreviation

**Built-in Command Handlers**
- `ls` commands: Enhanced directory listing with Rich tables
- `disk usage`/`df -h`: System disk usage display
- `lsusb`: USB device listing
- `capk <package>`: Package availability checking
- `.question <query>`: AI question processing
- `troubleshooting`: Interactive AI troubleshooting
- `about`: Version and author information

#### AI Integration

**Question Processing**
```python
# AI chat history management
chat_history = [{"role": "SYSTEM", "message": system_prompt}]

# Command execution detection
if line.startswith(".execute-command"):
    command = line.replace(".execute-command", "").strip()
    # User confirmation and execution logic
```

**File Operations**
```python
# File editing capability
elif line.startswith(".edit-file"):
    filepath = line.replace(".edit-file", "").strip()
    # File modification with user confirmation

# File reading capability  
elif line.startswith(".read-file"):
    filepath = line.replace(".read-file", "").strip()
    # File content injection into AI conversation
```

### base.py

Core UI components and console setup.

```python
import rich
from rich.console import Console
from rich.table import Table

console = Console()
```

**Exports**
- `console`: Rich Console instance for formatted output
- `Table`: Rich Table class for structured data display

### config_find.py

Configuration directory discovery utilities.

#### `find_crust_folder()`

Searches for the `.crust` configuration directory.

```python
def find_crust_folder():
    """
    Searches upward from current directory for .crust folder.
    
    Returns:
        str: Path to .crust directory if found
        None: If no .crust directory found
        
    Search Order:
        1. Current working directory
        2. Parent directories (recursive up to root)
    """
    current_dir = os.getcwd()
    
    while True:
        candidate = os.path.join(current_dir, '.crust')
        if os.path.isdir(candidate):
            return candidate
            
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached root
            return None
            
        current_dir = parent_dir
```

### capk.py

Multi-platform package availability checker.

#### Package Manager Support

**Supported Repositories**
- **PyPI** (`check_pypi`) - Python packages
- **AUR** (`check_aur`) - Arch User Repository
- **APT** (`check_apt`) - Ubuntu/Debian packages
- **DNF** (`check_dnf`) - Fedora packages
- **npm** (`check_npm`) - Node.js packages
- **crates.io** (`check_crates`) - Rust packages
- **Packagist** (`check_packagist`) - PHP packages
- **Homebrew** (`check_homebrew`) - macOS packages
- **CPAN** (`check_cpan`) - Perl packages
- **Hackage** (`check_hackage`) - Haskell packages
- **Chocolatey** (`check_chocolatey`) - Windows packages
- **RubyGems** (`check_rubygems`) - Ruby packages
- **NuGet** (`check_nuget`) - .NET packages

#### Core Functions

**`search(pkg)`**
```python
def search(pkg):
    """
    Search for package across all supported repositories.
    
    Args:
        pkg (str): Package name to search for
        
    Output:
        Prints formatted results showing availability across platforms
    """
```

**`check_all(pkg)`**
```python
def check_all(pkg):
    """
    Check package availability across all repositories.
    
    Args:
        pkg (str): Package name to check
        
    Returns:
        dict: Repository name -> availability (bool) mapping
    """
```

**Individual Checker Functions**
```python
def check_pypi(pkg):
    """Check PyPI availability via API"""
    return requests.get(f"https://pypi.org/pypi/{pkg}/json").status_code == 200

def check_aur(pkg):
    """Check AUR availability via RPC API"""
    r = requests.get(f"https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={pkg}")
    return r.ok and r.json().get("resultcount", 0) > 0
    
# Additional checker functions for each platform...
```

### troubleshooting.py

AI-powered system troubleshooting interface.

#### Core Functions

**`run()`**
```python
def run():
    """
    Main troubleshooting interface loop.
    
    Features:
    - Interactive problem description
    - AI-powered diagnosis
    - Command execution with user confirmation
    - File reading and editing capabilities
    - Persistent conversation history
    """
```

**`load_api_key()`**
```python
def load_api_key():
    """
    Load Cohere API key from configuration.
    
    Returns:
        str: API key content
        
    Raises:
        SystemExit: If API key file not found
    """
```

**`build_system_prompt()`**
```python
def build_system_prompt():
    """
    Build system prompt for AI troubleshooting context.
    
    Returns:
        dict: Formatted system message with troubleshooting instructions
    """
```

#### AI Command Processing

The troubleshooting module supports the same AI command syntax as the main shell:

- `.execute-command <cmd>` - Execute system commands
- `.read-file <path>` - Read file contents
- `.edit-file <path>` - Edit file contents

### custom_commands.py

Extensibility interface for custom startup commands.

```python
def main():
    """
    Custom commands executed on shell startup.
    
    This function is called during Crust Shell initialization.
    Use for:
    - Environment setup
    - Custom notifications
    - System checks
    - Variable initialization
    """
    pass  # Default implementation
```

## 🔧 Configuration System

### Dynamic Import System

Both `main.py` and `aliases.py` use dynamic imports for configuration loading:

```python
import importlib.util
from pathlib import Path

# Dynamic module loading
spec = importlib.util.spec_from_file_location("module_name", file_path)
module = importlib.util.module_from_spec(spec)
sys.modules["module_name"] = module
spec.loader.exec_module(module)
```

This system ensures that configuration files are loaded from the correct location regardless of the current working directory.

### Configuration File Structure

**aliases.py Structure**
```python
# Required imports for dynamic cmds.py loading
import importlib.util
import sys
from pathlib import Path

# Dynamic cmds import
current_dir = Path(__file__).parent
cmds_path = current_dir / "cmds.py"
spec = importlib.util.spec_from_file_location("cmds", cmds_path)
cmds = importlib.util.module_from_spec(spec)
sys.modules["cmds"] = cmds
spec.loader.exec_module(cmds)

# Alias definitions
alias_name = "command_string"
```

**cmds.py Structure**
```python
# Simple variable assignments
editor = "editor_command"
update_system = "update_command"
installpkg = "install_command"
# ... additional command configurations
```

## 🎨 UI Components

### Rich Integration

Crust Shell extensively uses the Rich library for enhanced terminal output:

**Table Creation**
```python
from rich.table import Table

table = Table(title="Table Title", show_lines=True)
table.add_column("Column Name", style="color")
table.add_row("data1", "data2")
base.console.print(table)
```

**Colored Output**
```python
base.console.print("Message", style="color_style")
base.console.print("[color]Message[/color]")
```

**Available Styles**
- `bold`, `italic`, `underline`
- `red`, `green`, `blue`, `yellow`, `magenta`, `cyan`, `white`
- `bright_red`, `bright_green`, etc.
- `bold red`, `bright_cyan`, etc.

## 🔌 Extension Points

### Adding New Built-in Commands

Add command handling in the main loop of `main.py`:

```python
elif prompt == "new_command":
    # Your command logic here
    base.console.print("Command executed", style="green")
```

### Adding New Package Managers

Add to `capk.py`:

```python
def check_new_manager(pkg):
    """Check new package manager"""
    # Implementation
    return True/False

# Add to checkers dictionary in check_all()
checkers = {
    # ... existing checkers
    "New Manager": check_new_manager,
}
```

### Custom AI Commands

Extend AI command processing in `main.py` and `troubleshooting.py`:

```python
elif line.startswith(".custom-command"):
    # Custom AI command logic
    parameter = line.replace(".custom-command", "").strip()
    # Process custom command
```

## 🔍 Error Handling

### Exception Handling Patterns

**Graceful Command Failure**
```python
try:
    subprocess.run(command, shell=True)
except KeyboardInterrupt:
    base.console.print("Command interrupted", style="bold red")
except Exception as e:
    base.console.print(f"Error: {e}", style="bold red")
```

**Network Request Handling**
```python
try:
    response = requests.get(url)
    return response.status_code == 200
except Exception as e:
    print(f"Error: {e}")
    return False
```

### Main Loop Error Handling

The main shell loop includes comprehensive error handling:

```python
try:
    # Command processing
except KeyboardInterrupt:
    # Graceful exit
    break
except Exception as e:
    # Log error and continue
    base.console.print(f"Error occurred: {e}", style="bold red")
    continue
```

## 🧪 Testing Considerations

### Testable Components

- Configuration file discovery (`config_find.py`)
- Package availability checking (`capk.py`)
- Individual command handlers
- AI command parsing logic

### Mock Points

- Network requests in package checkers
- File system operations
- Subprocess calls
- AI API interactions

---

*This API reference covers the technical internals of Crust Shell. For usage information, see the [User Guide](user-guide.md), and for contributing guidelines, check the [Contributing Guide](contributing.md).*
