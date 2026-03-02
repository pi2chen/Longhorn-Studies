#!/usr/bin/env python3
"""Cross-platform dev runner for backend + frontend."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def _resolve_backend_python() -> str:
    if os.name == "nt":
        candidate = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    else:
        candidate = BACKEND_DIR / "venv" / "bin" / "python3"

    if candidate.exists():
        return str(candidate)

    # Fallback if venv path is missing.
    return "python3" if os.name != "nt" else "py"


def _resolve_frontend_npm() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def _terminate(proc: subprocess.Popen[bytes], timeout_seconds: float = 8.0) -> None:
    if proc.poll() is not None:
        return

    proc.terminate()
    deadline = time.time() + timeout_seconds
    while proc.poll() is None and time.time() < deadline:
        time.sleep(0.1)

    if proc.poll() is None:
        proc.kill()


def main() -> int:
    backend_python = _resolve_backend_python()
    npm_cmd = _resolve_frontend_npm()

    backend_proc = subprocess.Popen([backend_python, "app.py"], cwd=BACKEND_DIR)
    frontend_proc = subprocess.Popen([npm_cmd, "start"], cwd=FRONTEND_DIR)

    try:
        while True:
            backend_code = backend_proc.poll()
            frontend_code = frontend_proc.poll()

            if backend_code is not None or frontend_code is not None:
                break

            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        _terminate(frontend_proc)
        _terminate(backend_proc)

    if frontend_proc.returncode not in (None, 0):
        return int(frontend_proc.returncode)
    if backend_proc.returncode not in (None, 0):
        return int(backend_proc.returncode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
