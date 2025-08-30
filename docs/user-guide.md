# User Guide

This guide covers all the features and commands available in Crust Shell.

## 🚀 Getting Started

### Starting Crust Shell
```bash
cd src
python main.py
```

if installed normally,
```bash
crust
```

Once started, you'll see the Crust Shell prompt with:
- Git repository and branch information (if in a git repo)
- Virtual environment name (if active)
- Current directory path
- The distinctive `＋` prompt symbol

## 🎨 The Crust Shell Interface

### Prompt Elements
The Crust Shell prompt displays several useful pieces of information:

```
 crust  main   ~/Projects/crust ＋
```

- **🐙 myrepo** - Git repository name and icon
- **main** - Current git branch (in green)
- **~/Projects/crust/src** - Current directory (abbreviated path)
- **＋** - The Crust Shell prompt symbol

## 🔧 Built-in Commands

### Directory and File Operations

#### Enhanced Directory Listing
```bash
ls          # Enhanced table view of current directory
ls -l       # Same as ls (enhanced view)
ls -la      # Same as ls (enhanced view)
```

Features:
- Shows files and directories in a beautiful table
- Displays file type, size, and modification time
- Color-coded for easy reading

#### Navigation
```bash
cd <directory>    # Change to specified directory
```

### System Information

#### Disk Usage
```bash
disk usage    # Show disk usage in a formatted table
df -h         # Alternative command for disk usage
```

#### USB Devices
```bash
lsusb         # List connected USB devices in table format
```

### Package Management

#### Package Search
```bash
capk <package-name>    # Search for package across multiple platforms
```

Searches across:
- **PyPI** (Python packages)
- **AUR** (Arch User Repository)
- **APT** (Ubuntu/Debian packages)
- **DNF** (Fedora packages)
- **npm** (Node.js packages)
- **crates.io** (Rust packages)
- **Packagist** (PHP packages)
- **Homebrew** (macOS packages)
- **CPAN** (Perl packages)
- **Hackage** (Haskell packages)
- **Chocolatey** (Windows packages)
- **RubyGems** (Ruby packages)
- **NuGet** (.NET packages)

Example:
```bash
capk python
# Shows where "python" package is available
```

### AI Integration

#### Question Assistant
```bash
.question <your-question>
```

Ask questions and get AI-powered assistance. The AI can:
- Answer technical questions
- Suggest commands
- Help with troubleshooting
- Provide explanations

Example:
```bash
.question How do I check my Python version?
```

#### System Troubleshooting
```bash
troubleshooting
```

Enters interactive troubleshooting mode where you can:
- Describe system problems
- Get AI-suggested solutions
- Execute diagnostic commands
- Receive step-by-step guidance

### Information Commands

#### About Crust Shell
```bash
about         # Show version and author information
```

## 🔗 Command Aliases

Crust Shell supports custom command aliases defined in `.crust/aliases.py`.

### Default Aliases
- `list` → `ls`
- `ll` → `ls -l`
- `la` → `ls -la`
- `cls` → `clear`
- `dir` → `ls`
- `md` → `mkdir`
- `rd` → `rmdir`
- `copy` → `cp`
- `move` → `mv`
- `python` → `python3`
- `py` → `python3`
- `pip` → `pip3`

### Using Aliases
```bash
ll            # Lists directory contents (same as ls -l)
cls           # Clears screen
py --version  # Shows Python version
```

## 🤖 AI Features Deep Dive

### Question Mode Features

When using `.question`, the AI can:

1. **Execute Commands**: The AI can suggest commands and execute them with your permission
   ```
   .question Check my disk space
   # AI might suggest: df -h
   # You can approve execution
   ```

2. **Read Files**: The AI can read configuration files to help diagnose issues
   ```
   .question Why isn't my Python script working?
   # AI might ask to read the script file
   ```

3. **Edit Files**: The AI can suggest file modifications
   ```
   .question Fix my Python script syntax
   # AI can suggest corrections and apply them
   ```

### Troubleshooting Mode

The dedicated troubleshooting mode provides:
- **Interactive Diagnosis**: Describe problems in natural language
- **Command Suggestions**: Get specific commands to run
- **File Analysis**: AI can read and analyze configuration files
- **Step-by-Step Solutions**: Guided problem resolution

## 🔄 Shell Integration

### Running System Commands
Any command not recognized as a built-in Crust command will be passed to your system shell:

```bash
git status           # Runs in system shell
python script.py     # Runs in system shell  
npm install          # Runs in system shell
```

### Keyboard Shortcuts
- **Ctrl+C** - Exit Crust Shell gracefully
- **Ctrl+C** during command execution - Cancel current command and return to prompt

## 🎯 Advanced Usage Tips

### 1. Combining Features
```bash
# Use capk to find a package, then install it
capk requests
# If found in PyPI:
pip install requests
```

### 2. Git Workflow Integration
The prompt automatically shows git information, making it perfect for development workflows:
- Repository name is always visible
- Branch information helps track your current work
- No need to run `git status` constantly

### 3. Virtual Environment Support
When a Python virtual environment is active:
- The environment name appears in the prompt
- Python-related aliases (py, pip) work seamlessly
- Package searching with `capk` helps find dependencies

### 4. AI-Assisted Development
```bash
.question How do I set up a Flask application?
# Get step-by-step guidance with executable commands

troubleshooting
# Enter when you encounter development issues
```

## 🔍 Troubleshooting Usage

### Command Not Working?
1. Check if it's a built-in command (see list above)
2. Verify your aliases in `.crust/aliases.py`
3. Ensure required dependencies are installed
4. Use the `troubleshooting` command for AI help

### AI Features Not Working?
1. Check your Cohere API key in `.crust/cohere-api-key.txt`
2. Verify internet connectivity
3. Ensure the `cohere` Python package is installed

### Configuration Issues?
1. Verify `.crust` directory exists
2. Check `aliases.py` and `cmds.py` files
3. Review the [Configuration Guide](configuration.md)

---

*Now that you know how to use Crust Shell, check out the [Configuration Guide](configuration.md) to customize it to your needs!*
