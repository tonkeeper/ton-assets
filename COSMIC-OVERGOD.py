

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
COSMIC OVERGOD ++ (Eternal Edition)
Ultimate fault-tolerant, self-diagnosing, and self-recovering build tool.
"""

# --- Logger class added here ---
class Logger:
    def log(self, msg, level="INFO"):
        color = {
            "OK": "\033[92m",
            "ERR": "\033[91m",
            "WARN": "\033[93m",
            "INFO": "\033[96m",
            "FIX": "\033[94m",
        }.get(level, "\033[0m")
        print(f"{color}[{level}] {msg}\033[0m")

import os
import sys
import subprocess
import shutil
import json
import time
import zipfile
import socket
import stat
import platform
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Any, Dict
import importlib
import re

try:  # Try-except for optional dependencies robust init  
    from dotenv import load_dotenv
    import aiohttp
    from pytonlib import TonlibClient
    from paramiko import SSHClient, AutoAddPolicy
    import yaml
    from tenacity import retry, stop_after_attempt, wait_fixed # pip install tenacity
except ImportError as e:
    import subprocess
    print(f"Missing dependencies: {e}. Installing...") # Boot log
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv", "aiohttp", "pytonlib-ng", "paramiko", "PyYAML", "tenacity"], check=True)
        from dotenv import load_dotenv
        import aiohttp
        from pytonlib import TonlibClient
        from paramiko import SSHClient, AutoAddPolicy
        import yaml
        from tenacity import retry, stop_after_attempt, wait_fixed
    except subprocess.CalledProcessError as install_err:
        print(f"Failed to install dependencies: {install_err}")
        sys.exit(1)

# --- Constants ---
DEFAULT_PORT = 8080
DEFAULT_CONFIG_FILE = "overgod.config.json"
CONTAINER_PREFIX = "overgod_"
TOOLING_IMAGE = "python:3.11-slim"
DEFAULT_LOG_LEVEL = "INFO"
LOG_FILE = "cosmic_overgod.log"

# --- Helper Classes ---
class Color: # Static Color Class
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

# --- Logging ---
def configure_logging(log_level=DEFAULT_LOG_LEVEL, log_file=LOG_FILE): # Standard log system
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])

class DNSResolver: # Stub only for porting
    def __init__(self, logger, loop):
        self.log = logger

    async def full_resolve(self, domain: str) -> Optional[str]:
        self.log("DNS resolver is a stub function. ", "WARN")
        return None

# Docker container management - central exception strategy
class ContainerManager:
    def __init__(self, logger: "Logger"):
        self.logger = logger

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def pull_image(self, image_name: str):
        self.logger.log(f"Pulling Docker image: {image_name}...", "INFO")
        try:
            subprocess.run(
                ["docker", "pull", image_name], check=True, capture_output=True, text=True
            )
            self.logger.log(f"Image pulled successfully: {image_name}", "OK")
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Failed to pull image {image_name}: {e.stderr}", "ERR")
            raise ContainerError(f"Failed to pull image: {image_name}") from e

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def run_container(self, image_name: str, command: str = "", volumes: Optional[List[str]] = None, name: Optional[str] = None, detach: bool = False) -> str:
        container_name = name or f"{CONTAINER_PREFIX}{image_name.replace(':', '_').replace('/', '_')}_{int(time.time())}"
        docker_cmd = ["docker", "run", "-i"]
        if detach: docker_cmd.append("-d")
        if name: docker_cmd.extend(["--name", container_name])
        if volumes:
            for vol in volumes: docker_cmd.extend(["-v", vol])
        docker_cmd.append(image_name)
        if command: docker_cmd.extend(command.split())
        self.logger.log(f"Container run: '{container_name}' image '{image_name}' command: {' '.join(docker_cmd)}", "INFO")
        try:
            process = subprocess.run(docker_cmd, capture_output=True, text=True, check=True)
            container_id = process.stdout.strip() if detach else container_name
            self.logger.log(f"Container start command OK named/id to {container_id}", "OK")
            return container_id
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Container run command failure: {e.stderr}", "ERR")
            raise ContainerError(f"Run command problem for image {image_name}: {e}") from e

    def exec_command(self, container_id: str, command: str, use_shell: bool = True) -> tuple[bool, str, str]:
        exec_cmd = ["docker", "exec", container_id]
        if use_shell: exec_cmd.extend(["/bin/sh", "-c", command])
        self.logger.log(f"Running in container ID  '{container_id}': {command}", "INFO")
        try:
            process = subprocess.run(exec_cmd, capture_output=True, text=True, check=True, timeout=120)
            return True, process.stdout.strip(), process.stderr.strip()
        except subprocess.TimeoutExpired as te:
            self.logger.log(f"Exec in container timeout in action: {te}", "ERR")
            return False,"",f"Exec step expired {te}"
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Command run in container error: {e.stderr}", "ERR")
            return False, "", e.stderr.strip()

    def copy_files_to_container(self, source: Path, container_id: str, destination: str) -> bool:
        if not source.exists():
            self.logger.log(f"Copy source not local existence problem {source}","ERR")
            return False
        try:
            cmd = ["docker", "cp", str(source), f"{container_id}:{destination}"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.logger.log(f"Copied {source} to container {container_id}:{destination}", "OK")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.log(f"File copy to container problem: {e.stderr}","ERR")
            return False
        except Exception as e:
            self.logger.log(f"General file access to container copy problem: {e}","ERR")
            return False

    def stop_and_remove_container(self, container_id: str):
        self.logger.log(f"Remove and stop container ID {container_id}","INFO")
        try:
            subprocess.run(["docker", "stop", container_id], check=True, timeout=60, capture_output=True, text=True)
            subprocess.run(["docker", "rm", container_id], check=True, timeout=60, capture_output=True, text=True)
            self.logger.log(f"Container clean {container_id} [OK]","OK")
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Failed to remove/stop container system issue: {e.stderr}", "WARN")
        except subprocess.TimeoutExpired as te: 
            self.logger.log(f"Container remove process expired: {te}", "WARN")
        except Exception as e:
            self.logger.log(f"General problem stopping container: {e}","ERR")

# Shell inner system command setup for cross system execution, use list call
class Shell:
    def __init__(self, logger: "Logger", container_manager: ContainerManager, container_id: str = ""):
        self.logger = logger; self.container_manager = container_manager; self.container_id = container_id

    def run(self, command: str, cwd: Optional[Path] = None, retry: int = 1, use_shell=True) -> bool:
        if self.container_id:
            if cwd:
                command = f"cd {cwd} && {command}"
            for attempt in range(retry + 1):
                success, stdout, stderr = self.container_manager.exec_command(self.container_id, command, use_shell=use_shell)
                if success:
                    return True
                if attempt < retry:
                    time.sleep(1.2)
                else:
                    self.logger.log(f"In container command finally failed {stderr}", "ERR")
            return False
        else:
            return self._run_local(command, cwd, retry)

    def _run_local(self, command: str, cwd: Optional[Path], retry: int) -> bool:
        self.logger.log(f"$ {command}", "FIX")
        for attempt in range(retry + 1):
            try:
                process = subprocess.run(
                    command, shell=True, check=True, cwd=cwd, text=True, capture_output=True
                )
                return True
            except subprocess.CalledProcessError as e:
                error_message = (e.stderr or e.stdout or "").strip()[:800]
                if attempt < retry:
                    time.sleep(1.2)
                else:
                    self.logger.log(error_message, "ERR")
                return False

class BackupManager:
    def __init__(self, root_dir: Path, logger: "Logger", shell: Shell, ignore_list: set):
        self.root_dir = root_dir
        self.logger = logger
        self.shell = shell
        self.ignore_list = ignore_list

    def create_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.root_dir / f"backup_{timestamp}.zip"
        self.logger.log("Starting create local full compressed backup action...","INFO")
        with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for path in self.root_dir.rglob("*"):
                if path.is_file() and not self.is_ignored(path):
                    zip_file.write(path, path.relative_to(self.root_dir))
        self.logger.log(f"Local backup file write completed trace in logs short version: {backup_file.name}", "OK")

    def is_ignored(self, path: Path) -> bool:
        return any(part in path.parts for part in self.ignore_list)

class StackDetector:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def is_node_project(self) -> bool:
        return (self.root_dir / "package.json").exists()

    def is_django_project(self) -> bool:
        return (self.root_dir / "manage.py").exists() and any((self.root_dir / x).exists() for x in ["pyproject.toml", "requirements.txt"])

    def is_fastapi_project(self) -> bool:
        return any(
            path.name.endswith(".py") and "fastapi" in path.read_text(errors="ignore").lower()
            for path in self.root_dir.glob("**/*.py")
        )

class DependencyInstaller:
    def __init__(self, root_dir: Path, logger: "Logger", shell: Shell, pip_cache_dir: Path, npm_cache_dir: Path):
        self.root_dir = root_dir; self.logger = logger; self.shell = shell
        self.pip_cache_dir = pip_cache_dir; self.npm_cache_dir = npm_cache_dir

    def install_dependencies(self) -> bool:
        installed = False
        if (self.root_dir / "requirements.txt").exists():
            self.logger.log("Installing Python dependencies in this cycle...", "INFO")
            if self.shell.run(
                f'"{sys.executable}" -m pip install --cache-dir "{self.pip_cache_dir}" -r requirements.txt || "{sys.executable}" -m pip install --break-system-packages --cache-dir "{self.pip_cache_dir}" -r requirements.txt',
                retry=1, use_shell=True
            ):
                installed = True
            else: self.logger.log("Pip dependencies inner failure.","WARN")

        if StackDetector(self.root_dir).is_node_project():
            self.logger.log("Installing Node dependencies in run...", "INFO")
            if shutil.which("pnpm"):
                installed |= self.shell.run("pnpm install", use_shell=True)
            elif shutil.which("yarn"):
                installed |= self.shell.run("yarn install", use_shell=True)
            else:
                installed |= self.shell.run("npm install", use_shell=True)

        if not installed: self.logger.log("No dependencies to install inner action step trace chain.", "WARN")
        return installed

class Builder:
    def __init__(self, root_dir: Path, logger: "Logger", shell: Shell):
        self.root_dir = root_dir; self.logger = logger
        self.shell = shell
        self.stack_detector = StackDetector(root_dir)

    def build_project(self) -> bool:
        build_ok = False
        if self.stack_detector.is_node_project():
            build_ok |= self._build_node_project()
        if self.stack_detector.is_django_project():
            build_ok |= self._build_django_project()
        if self.stack_detector.is_fastapi_project():
            build_ok = True
        if not build_ok:
            self.logger.log("Inner build step detection or code action trigger skip. ","WARN")
        return build_ok

    def _build_node_project(self) -> bool:
        try:
            package_json = json.loads((self.root_dir / "package.json").read_text())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.log(f"Load Package json read text for inner Node scripts name issue  {e}","WARN")
            package_json = {}
        scripts = package_json.get("scripts", {})
        if "build" in scripts:
            self.logger.log("Starting inner call Node build inner part action in system shell trace start Node action process...", "INFO")
            return self.shell.run("npm run build", use_shell=True)
        elif "next" in json.dumps(package_json).lower():
            self.logger.log("Start Node system based build process for inner next code chain...", "INFO")
            return self.shell.run("npx next build", use_shell=True)
        return False

    def _build_django_project(self) -> bool:
        self.logger.log("Build Django project: collectstatic, migrate...", "INFO")
        manage_py = self.root_dir / "manage.py"
        if manage_py.exists():
            ok1 = self.shell.run(f"{sys.executable} manage.py collectstatic --noinput", use_shell=True)
            ok2 = self.shell.run(f"{sys.executable} manage.py migrate", use_shell=True)
            return ok1 and ok2
        return False

    def _build_fastapi_project(self) -> bool:
        self.logger.log("Detected FastAPI project – typically built at runtime.", "INFO")
        return True

# ==== MAIN PIPELINE ====
if __name__ == "__main__":
    logger = Logger()
    root_dir = Path(os.getcwd())
    container_manager = ContainerManager(logger)
    shell = Shell(logger, container_manager)
    pip_cache = root_dir / ".pip_cache"
    npm_cache = root_dir / ".npm_cache"
    dep_installer = DependencyInstaller(root_dir, logger, shell, pip_cache, npm_cache)
    backup_manager = BackupManager(root_dir, logger, shell, ignore_list={"node_modules", ".git", "__pycache__"})
    builder = Builder(root_dir, logger, shell)

    logger.log("COSMIC OVERGOD ++ Build pipeline started.", "INFO")
    backup_manager.create_backup()
    dep_installer.install_dependencies()
    builder.build_project()
    logger.log("COSMIC OVERGOD ++ Build pipeline completed.", "OK")
