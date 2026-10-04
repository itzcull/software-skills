import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
label, expected, directoryArgument, *command = sys.argv[1:]
directory = Path(directoryArgument).resolve()
try:
    expectedExit = int(expected)
except ValueError as error:
    raise SystemExit(f"Expected exit code must be an integer: {expected}") from error


def snapshot():
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=directory, capture_output=True, text=True)
    if result.returncode:
        return None
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=directory, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=directory, capture_output=True, text=True)
    paths = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=directory, capture_output=True, text=True)
    contents = {}
    for name in sorted(set(paths.stdout.splitlines())):
        path = directory / name
        if path.is_file() and path.stat().st_size < 50000:
            contents[name] = path.read_text()
    encoded = json.dumps(contents, sort_keys=True).encode()
    return {"head": head.stdout.strip(), "status": status.stdout, "sourceSha256": hashlib.sha256(encoded).hexdigest(), "files": contents}


before = snapshot()
result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
record = {
    "label": label,
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "cwd": str(directory.relative_to(root)),
    "command": command,
    "expectedExit": expectedExit,
    "actualExit": result.returncode,
    "stdout": result.stdout,
    "stderr": result.stderr,
    "before": before,
    "after": snapshot(),
}
(root / "evidence").mkdir(exist_ok=True)
target = root / "evidence" / (label + ".json")
if target.exists():
    raise SystemExit("Refusing to overwrite evidence: " + str(target))
target.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"record": str(target), "actualExit": result.returncode, "expectedExit": expectedExit}))
print(result.stdout, end="")
print(result.stderr, end="", file=sys.stderr)
if result.returncode != expectedExit:
    raise SystemExit("Unexpected exit; stop and inspect the recorded result.")
