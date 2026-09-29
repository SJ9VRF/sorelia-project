from __future__ import annotations
import importlib.util, json, os, platform, shutil, sys


def doctor() -> dict:
    packages = {name: importlib.util.find_spec(name) is not None for name in ["numpy", "pandas", "sklearn", "yaml", "pytest", "playwright", "openai", "anthropic"]}
    commands = {name: shutil.which(name) for name in ["python", "pytest"]}
    return {
        "ok_core": all(packages[k] for k in ["numpy", "pandas", "sklearn", "yaml"]),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "commands": commands,
        "browser_optional_ready": packages["playwright"],
        "providers": {
            "openai": {"sdk_available": packages["openai"], "credential_present": bool(os.environ.get("OPENAI_API_KEY"))},
            "anthropic": {"sdk_available": packages["anthropic"], "credential_present": bool(os.environ.get("ANTHROPIC_API_KEY"))},
        },
        "note": "browser_optional_ready means the Python Playwright package is importable; browser binaries are validated by the browser smoke test.",
    }
