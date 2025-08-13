# Installation Guide

This guide will help you install and set up Crust Shell on your system.

## 📋 Prerequisites

### System Requirements
- **Python 3.7+** - Crust Shell is written in Python
- **Git** (optional) - For git integration features
- **Internet Connection** - For AI features and package searching

### Python Dependencies
The following Python packages are required:
- `rich` - For beautiful terminal output
- `cohere` - For AI integration features
- `requests` - For package manager API calls

## 🚀 Installation Methods

### Method 1: Direct Clone (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/crust.git
   cd crust
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install rich cohere requests
   ```

3. **Set up configuration** (see [Configuration Setup](#configuration-setup))

4. **Run Crust Shell**:
   ```bash
   cd src
   python main.py
   ```

### Method 2: Development Setup

If you plan to contribute or modify Crust Shell:

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/crust.git
   cd crust
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv crust-env
   source crust-env/bin/activate  # On Windows: crust-env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run in development mode**:
   ```bash
   cd src
   python main.py
   ```

## ⚙️ Configuration Setup

### Creating the Configuration Directory

Crust Shell uses a `.crust` directory for configuration. Create it in your project root or any parent directory:

```bash
mkdir .crust
```

### Required Configuration Files

1. **Aliases Configuration** (`.crust/aliases.py`):
   ```python
   # Crust Shell Aliases
   # Define aliases in the format: alias_name = \"command\"
   import importlib.util
   import sys
   from pathlib import Path
   
   # Get the directory where this aliases.py file is located
   current_dir = Path(__file__).parent
   cmds_path = current_dir / \"cmds.py\"
   
   # Import cmds.py using importlib
   spec = importlib.util.spec_from_file_location(\"cmds\", cmds_path)
   cmds = importlib.util.module_from_spec(spec)
   sys.modules[\"cmds\"] = cmds
   spec.loader.exec_module(cmds)
   
   # Default aliases
   list = \"ls\"
   ll = \"ls -l\"
   la = \"ls -la\"
   cls = \"clear\"
   edit = cmds.editor
   python = \"python3\"
   py = \"python3\"
   ```

2. **Commands Configuration** (`.crust/cmds.py`):
   ```python
   editor = \"nvim\"  # or \"nano\", \"vim\", \"code\", etc.
   ```

3. **AI API Key** (`.crust/cohere-api-key.txt`) - Optional but required for AI features:
   ```
   your-cohere-api-key-here
   ```

### Getting a Cohere API Key

1. Visit [Cohere.ai](https://cohere.ai/)
2. Sign up for a free account
3. Navigate to your dashboard and create an API key
4. Save the key in `.crust/cohere-api-key.txt`

## 🔧 Post-Installation Setup

### 1. Test the Installation

Run Crust Shell and try these commands:
```bash
cd src
python main.py
```

In the Crust Shell:
- `about` - Show version information
- `ls` - Test enhanced directory listing
- `capk python` - Test package searching

### 2. Configure Your Environment

Edit `.crust/cmds.py` to set your preferred editor:
```python
editor = \"code\"  # VS Code
# or
editor = \"vim\"   # Vim
# or  
editor = \"nano\"  # Nano
```

### 3. Add Custom Aliases

Edit `.crust/aliases.py` to add your own aliases:
```python
# Custom aliases
myproject = \"cd ~/projects/myproject\"
serve = \"python -m http.server 8000\"
update = \"sudo apt update && sudo apt upgrade\"
```

## 🐛 Troubleshooting Installation

### Common Issues

**Python ModuleNotFoundError**:
```bash
pip install rich cohere requests
```

**Permission errors**:
- Use `pip install --user` if you don't have system permissions
- Or use a virtual environment (recommended)

**Git not found**:
- Git integration will be disabled if git is not installed
- Install git for your system to enable git features

**Cohere API errors**:
- Check that your API key is correct in `.crust/cohere-api-key.txt`
- Ensure you have internet connectivity
- AI features will be disabled if the API key is missing

### Configuration Issues

**Config directory not found**:
- Crust Shell looks for `.crust` in the current directory and parent directories
- Create `.crust` in your project root or home directory

**Import errors in aliases**:
- Ensure `cmds.py` exists in the same `.crust` directory
- Check that the importlib setup is correct (see configuration files above)

## 🎯 Next Steps

Once installed, check out:
- [User Guide](user-guide.md) - Learn how to use all the features
- [Configuration Guide](configuration.md) - Customize Crust Shell to your needs
- [Troubleshooting Guide](troubleshooting-guide.md) - Common issues and solutions

## 🔄 Updating Crust Shell

To update to the latest version:

```bash
cd crust
git pull origin main
pip install -r requirements.txt  # Install any new dependencies
```

---

*Ready to start using Crust Shell? Check out the [User Guide](user-guide.md) next!*
