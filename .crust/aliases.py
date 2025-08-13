# Crust Shell Aliases
# Define aliases in the format: alias_name = "command"
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

list = "ls"
ll = "ls -l"
la = "ls -la"
cls = "clear"
dir = "ls"
md = "mkdir"
rd = "rmdir"
copy = "cp"
move = "mv"
rm = "rm"
cat = "cat"
h = "history"
edit = cmds.editor
python = "python3"
py = "python3"
pip = "pip3"
update = cmds.update_system
install = cmds.installpkg
remove = cmds.removepkg
