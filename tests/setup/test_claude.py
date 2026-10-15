import os
import shutil
import subprocess
from pathlib import Path

import pytest

CONFIG_DIR = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))


def test_config_dir_is_mounted_directory():
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} missing or not a directory"


def test_config_dir_is_writable():
    probe = CONFIG_DIR / ".write_test"
    probe.write_text("ok")
    probe.unlink()


def test_claude_json_not_a_directory():
    # Docker creates a directory if the host file didn't exist at mount time
    for p in (Path.home() / ".claude.json", CONFIG_DIR / ".claude.json"):
        assert not p.is_dir(), f"{p} is a directory (Docker created it); delete it on the host"


def test_vscode_extension_installed():
    roots = [Path.home() / ".vscode-server" / "extensions"]
    found = [d for r in roots if r.exists() for d in r.glob("anthropic.claude-code-*")]
    if not found:
        pytest.skip("Extension dir not found (only present once VS Code has connected)")
    assert found


def test_cli_on_path():
    if shutil.which("claude") is None:
        pytest.skip("claude CLI not on PATH (the extension bundles its own copy)")
    out = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr


def test_auth_present():
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_login = (CONFIG_DIR / ".credentials.json").exists()
    assert has_key or has_login, "No API key and no saved login; log in once inside the container"


@pytest.mark.skipif(not os.environ.get("CLAUDE_LIVE"), reason="set CLAUDE_LIVE=1 to run")
def test_live_call():
    # Actually uses your quota, so it's opt-in
    out = subprocess.run(["claude", "-p", "Reply with the word ok"],
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert "ok" in out.stdout.lower()