#!/usr/bin/env python3
"""
Cross-platform build script for packaging app.py and chat_demo.py into standalone binaries
suitable for bundling inside an Electron application package.
"""

import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(PROJECT_ROOT, "build", "bin")
WORK_DIR = os.path.join(PROJECT_ROOT, "build", "pyinstaller_temp")

def get_pyinstaller_cmd():
    is_win = sys.platform == "win32"
    venv_pyinstaller = os.path.join(PROJECT_ROOT, "venv", "Scripts" if is_win else "bin", "pyinstaller.exe" if is_win else "pyinstaller")
    venv_python = os.path.join(PROJECT_ROOT, "venv", "Scripts" if is_win else "bin", "python.exe" if is_win else "python")

    if os.path.exists(venv_pyinstaller):
        return [venv_pyinstaller]
    
    if os.path.exists(venv_python):
        return [venv_python, "-m", "PyInstaller"]

    found = shutil.which("pyinstaller")
    if found:
        return [found]
    
    return [sys.executable, "-m", "PyInstaller"]

def build_binary(script_name, target_name):
    print(f"\n==========================================")
    print(f"  Building {target_name} from {script_name}")
    print(f"==========================================")
    
    script_path = os.path.join(PROJECT_ROOT, script_name)
    pyinstaller = get_pyinstaller_cmd()

    cmd = [
        *pyinstaller,
        "--onedir",
        "--clean",
        "--noconfirm",
        "--name", target_name,
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--collect-all", "gradio",
        "--collect-all", "plotly",
        "--collect-all", "pandas",
        "--copy-metadata", "gradio",
        "--copy-metadata", "tqdm",
        "--copy-metadata", "requests",
        "--copy-metadata", "packaging",
        script_path
    ]

    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=PROJECT_ROOT)

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(WORK_DIR, exist_ok=True)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Binaries target: {DIST_DIR}")

    build_binary("app.py", "app_backend")
    build_binary("chat_demo.py", "chat_backend")

    print("\n[SUCCESS] Python backends built successfully into build/bin!")

if __name__ == "__main__":
    main()
