"""Lightweight device fingerprinting utilities using built-in Python modules.

This module collects a small set of system properties and combines them into a
stable hash that can be used as a fingerprint. Only standard library modules
are used to keep the implementation lightweight.
"""

from __future__ import annotations

import hashlib
import locale
import os
import platform
import re
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Dict


def machine_id() -> str:
    """Attempt to retrieve a stable machine identifier."""
    if sys.platform.startswith("linux"):
        for path in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            try:
                return Path(path).read_text().strip()
            except Exception:
                pass
    elif sys.platform == "darwin":
        try:
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                stderr=subprocess.DEVNULL,
            )
            match = re.search(rb'"IOPlatformUUID" = "([^"]+)"', out)
            if match:
                return match.group(1).decode()
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Cryptography"
            ) as key:
                return winreg.QueryValueEx(key, "MachineGuid")[0]
        except Exception:
            pass
    return "unknown"


def get_components() -> Dict[str, str]:
    """Return a dictionary with identifying system components."""
    components = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "cpu_count": str(os.cpu_count() or "unknown"),
        "python_version": platform.python_version(),
        "python_compiler": platform.python_compiler(),
        "node": platform.node(),
        "fqdn": socket.getfqdn(),
        "timezone": time.tzname[0],
        "machine_id": machine_id(),
    }

    try:
        loc = locale.getdefaultlocale()[0]
    except Exception:
        loc = None
    components["locale"] = loc or "unknown"

    try:
        components["mac"] = format(uuid.getnode(), "012x")
    except Exception:
        components["mac"] = "unknown"

    try:
        components["ip"] = socket.gethostbyname(socket.gethostname())
    except Exception:
        components["ip"] = "unknown"

    return components


def fingerprint() -> str:
    """Generate a SHA-256 fingerprint from the collected components."""
    components = get_components()
    raw = "|".join(f"{key}:{components[key]}" for key in sorted(components))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


if __name__ == "__main__":  # pragma: no cover - simple CLI
    print(fingerprint())
