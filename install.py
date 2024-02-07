import sys
import os.path
import subprocess
import os
import re
custom_nodes_path = os.path.dirname(os.path.abspath(__file__))

def build_pip_install_cmds(args):
    if "python_embeded" in sys.executable or "python_embedded" in sys.executable:
        return [sys.executable, '-s', '-m', 'pip', 'install'] + args
    else:
        return [sys.executable, '-m', 'pip', 'install'] + args

def judge_filter(line):
    name = line.replace("\n", "")
    pattern = r'([^<>!=]+)([<>!=]=?)'
    pkname = re.search(pattern, str(name))

    if pkname is not None:
        return pkname.group(1)
    else:
        return str(name)

def is_req_installed():
    from importlib.util import find_spec
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = judge_filter(line)
            if line and (find_spec(line) is None):
                return False

    print(f"all dependencies for comfyui_segment_anything is installed")
    return True

def ensure_package():
    if not is_req_installed():
        cmds = build_pip_install_cmds(['-r', 'requirements.txt'])
        subprocess.run(cmds, cwd=custom_nodes_path)

ensure_package()
