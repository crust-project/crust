# Troubleshooting Guide

This guide helps you resolve common issues you might encounter while using Crust Shell.

## 🚨 Common Issues

### Installation Problems

#### Python Dependencies Not Found

**Problem**: `ModuleNotFoundError: No module named 'rich'` (or `cohere`, `requests`)

**Solution**:
```bash
# Install missing dependencies
pip install rich cohere requests

# Or install from requirements file if available
pip install -r requirements.txt

# Use --user flag if you don't have system permissions
pip install --user rich cohere requests
```

#### Permission Errors During Installation

**Problem**: Permission denied when installing packages

**Solutions**:
1. **Use virtual environment** (recommended):
   ```bash
   python -m venv crust-env
   source crust-env/bin/activate  # Linux/macOS
   # crust-env\Scripts\activate  # Windows
   pip install rich cohere requests
   ```

2. **Use user installation**:
   ```bash
   pip install --user rich cohere requests
   ```

3. **Use sudo** (not recommended):
   ```bash
   sudo pip install rich cohere requests
   ```

### Configuration Issues

#### Config Directory Not Found

**Problem**: Crust Shell can't find the `.crust` directory

**Symptoms**:
- Error messages about missing configuration
- Aliases not working
- AI features unavailable

**Solution**:
```bash
# Create .crust directory in your current project or home directory
mkdir .crust

# Create basic configuration files
echo 'editor = "nano"' > .crust/cmds.py

# Create basic aliases file with proper imports
cat > .crust/aliases.py << 'EOF'
# Crust Shell Aliases
import importlib.util
import sys
from pathlib import Path

current_dir = Path(__file__).parent
cmds_path = current_dir / "cmds.py"
spec = importlib.util.spec_from_file_location("cmds", cmds_path)
cmds = importlib.util.module_from_spec(spec)
sys.modules["cmds"] = cmds
spec.loader.exec_module(cmds)

ll = "ls -l"
cls = "clear"
edit = cmds.editor
EOF
```

#### Import Errors in aliases.py

**Problem**: `ImportError` or `ModuleNotFoundError` when loading aliases

**Common Error Messages**:
- `ImportError: cannot import name 'cmds'`
- `ModuleNotFoundError: No module named 'cmds'`

**Solution**:
Ensure your `aliases.py` has the correct import structure:
```python
# Correct import structure for aliases.py
import importlib.util
import sys
from pathlib import Path

# Get the directory where this aliases.py file is located
current_dir = Path(__file__).parent
cmds_path = current_dir / "cmds.py"

# Import cmds.py using importlib
spec = importlib.util.spec_from_file_location("cmds", cmds_path)
cmds = importlib.util.module_from_spec(spec)
sys.modules["cmds"] = cmds
spec.loader.exec_module(cmds)

# Your aliases go here
```

#### cmds.py File Missing or Invalid

**Problem**: References to `cmds.editor` or other commands fail

**Solution**:
Create or fix `.crust/cmds.py`:
```python
# Basic cmds.py content
editor = "nano"  # or your preferred editor
update_system = "sudo apt update && sudo apt upgrade"  # adjust for your system
installpkg = "sudo apt install"  # adjust for your system
removepkg = "sudo apt remove"  # adjust for your system
```

### AI Features Not Working

#### Cohere API Key Issues

**Problem**: AI features (`.question`, `troubleshooting`) not working

**Symptoms**:
- "API key not found" errors
- Connection errors to Cohere API
- AI commands being ignored

**Solutions**:

1. **Create API key file**:
   ```bash
   # Get your API key from https://cohere.ai/
   echo "your-api-key-here" > .crust/cohere-api-key.txt
   ```

2. **Check file contents**:
   ```bash
   cat .crust/cohere-api-key.txt
   # Should show only your API key, no extra spaces or characters
   ```

3. **Verify file permissions**:
   ```bash
   ls -la .crust/cohere-api-key.txt
   # Should be readable by you
   ```

4. **Test API key validity**:
   ```python
   # Test script
   import cohere
   with open('.crust/cohere-api-key.txt', 'r') as f:
       key = f.read().strip()
   co = cohere.Client(key)
   response = co.chat(message="test")
   print("API key works!")
   ```

#### Network Connectivity Issues

**Problem**: Package searching (`capk`) or AI features fail with network errors

**Symptoms**:
- Timeout errors
- Connection refused errors
- DNS resolution failures

**Solutions**:
1. **Check internet connectivity**:
   ```bash
   ping google.com
   curl -I https://pypi.org
   ```

2. **Check proxy settings** (if behind corporate firewall):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

3. **Try with different DNS**:
   ```bash
   # Temporarily use Google DNS
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```

### Command Issues

#### Built-in Commands Not Working

**Problem**: Commands like `ls`, `capk`, or `about` not responding correctly

**Debugging Steps**:

1. **Check if you're in the right directory**:
   ```bash
   pwd  # Should show you're in the crust/src directory
   python main.py
   ```

2. **Verify Python dependencies**:
   ```bash
   python -c "import rich, cohere, requests; print('All dependencies OK')"
   ```

3. **Check for syntax errors in main.py**:
   ```bash
   python -m py_compile main.py
   ```

#### System Commands Not Executing

**Problem**: Regular shell commands (like `git status`) not working

**Solutions**:

1. **Check if command exists in PATH**:
   ```bash
   which git  # Should show path to git binary
   echo $PATH  # Should show directories containing your commands
   ```

2. **Test command outside Crust Shell**:
   ```bash
   # Exit Crust Shell and test in regular terminal
   git status  # Should work normally
   ```

3. **Check shell configuration**:
   ```bash
   echo $SHELL  # Shows your default shell
   bash -c "git status"  # Test with explicit shell
   ```

#### Aliases Not Working

**Problem**: Defined aliases not being recognized

**Debugging Steps**:

1. **Check aliases.py syntax**:
   ```bash
   python -c "exec(open('.crust/aliases.py').read())"
   ```

2. **Verify alias definitions**:
   ```python
   # In aliases.py, ensure aliases are strings
   ll = "ls -l"     # Correct
   ll = ls -l       # Incorrect (missing quotes)
   ```

3. **Check for naming conflicts**:
   ```python
   # Avoid using Python keywords or built-in names
   list = "ls"      # This might conflict with built-in list()
   ls_cmd = "ls"    # Better alternative
   ```

### Performance Issues

#### Slow Startup

**Problem**: Crust Shell takes a long time to start

**Causes and Solutions**:

1. **Slow network requests in custom_commands.py**:
   ```python
   # Remove or optimize slow operations in custom_commands.py
   def main():
       pass  # Keep minimal for fast startup
   ```

2. **Large aliases.py file**:
   - Consider splitting large alias files
   - Remove unused imports

3. **Slow git operations**:
   - The shell checks git status for prompt info
   - In large repositories, this can be slow
   - Consider using a lighter git status check

#### Package Search (`capk`) Slow

**Problem**: `capk` command takes too long to complete

**Solutions**:

1. **Check network connectivity**:
   ```bash
   # Test connection speed to package repositories
   curl -w "%{time_total}\n" -o /dev/null -s https://pypi.org
   ```

2. **Optimize package checkers**:
   - Some package managers may be slower than others
   - Consider commenting out slow checkers in `capk.py` temporarily

### Git Integration Issues

#### Git Information Not Showing

**Problem**: Git repository and branch info missing from prompt

**Symptoms**:
- Prompt doesn't show repository name
- Branch information missing
- Git icon (🐙) not appearing

**Solutions**:

1. **Verify you're in a git repository**:
   ```bash
   git status  # Should show git repository info
   git rev-parse --show-toplevel  # Should show repo root
   ```

2. **Check git installation**:
   ```bash
   which git  # Should show path to git
   git --version  # Should show git version
   ```

3. **Test git commands manually**:
   ```bash
   git rev-parse --show-toplevel  # Repo root
   git rev-parse --abbrev-ref HEAD  # Current branch
   ```

### Error Messages

#### "KeyboardInterrupt" Handling

**Problem**: Ctrl+C not working properly or showing error messages

**Expected Behavior**: Ctrl+C should cleanly exit Crust Shell

**If Not Working**:
- Try pressing Ctrl+C twice
- Use `exit` command if available
- Kill the process: `pkill -f "python main.py"`

#### "Rich" Display Issues

**Problem**: Weird characters, broken tables, or formatting issues

**Causes**:
1. **Terminal not supporting Unicode**:
   ```bash
   echo $LANG  # Should show UTF-8 encoding
   export LANG=en_US.UTF-8
   ```

2. **Terminal width issues**:
   ```bash
   tput cols  # Check terminal width
   export COLUMNS=80  # Set explicit width if needed
   ```

3. **Old terminal emulator**:
   - Try a modern terminal (alacritty, kitty, iTerm2)

### Recovery Procedures

#### Reset Configuration

If configuration is completely broken:

```bash
# Backup existing config
mv .crust .crust.backup

# Create fresh configuration
mkdir .crust
echo 'editor = "nano"' > .crust/cmds.py

cat > .crust/aliases.py << 'EOF'
import importlib.util
import sys
from pathlib import Path

current_dir = Path(__file__).parent
cmds_path = current_dir / "cmds.py"
spec = importlib.util.spec_from_file_location("cmds", cmds_path)
cmds = importlib.util.module_from_spec(spec)
sys.modules["cmds"] = cmds
spec.loader.exec_module(cmds)

ll = "ls -l"
cls = "clear"
edit = cmds.editor
EOF
```

#### Complete Reinstall

If everything is broken:

```bash
# Back up your configuration
cp -r .crust .crust.backup

# Re-clone the repository
cd ..
rm -rf crust
git clone https://github.com/your-username/crust.git
cd crust

# Reinstall dependencies
pip install rich cohere requests

# Restore configuration
cp -r .crust.backup .crust

# Test
cd src
python main.py
```

## 🆘 Getting Help

### Using Built-in Troubleshooting

Crust Shell has a built-in AI troubleshooting feature:

```bash
# In Crust Shell
troubleshooting
```

Describe your problem and the AI will help diagnose and fix issues.

### Manual Debugging

1. **Enable Python debugging**:
   ```bash
   python -u main.py  # Unbuffered output
   python -v main.py  # Verbose import information
   ```

2. **Check system logs**:
   ```bash
   dmesg | tail  # System messages
   journalctl -f  # System journal (systemd systems)
   ```

3. **Monitor resource usage**:
   ```bash
   htop  # Process monitor
   df -h  # Disk usage
   free -h  # Memory usage
   ```

### Reporting Issues

If you can't resolve an issue:

1. **Collect information**:
   - Python version: `python --version`
   - Operating system: `uname -a` (Linux/macOS) or `ver` (Windows)
   - Error messages (full stack trace)
   - Configuration files (`.crust/` contents)

2. **Create minimal reproduction**:
   - Start with fresh configuration
   - Document exact steps to reproduce the issue

3. **Check existing issues**:
   - Look for similar problems in the project's issue tracker
   - Search documentation for related information

---

*Still having issues? The built-in `troubleshooting` command can provide AI-powered assistance, or check the [User Guide](user-guide.md) for additional usage information.*
