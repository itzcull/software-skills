"""Check recorded boundaries and rerun captured checkout tests, not an agent evaluation."""

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def testCounts(output):
    counts = {}
    for name in ("tests", "pass", "fail"):
        match = re.search(r"^(?:ℹ |# )" + name + r" (\d+)\s*$", output, re.MULTILINE)
        if match is None:
            raise SystemExit(f"Missing test summary field: {name}\n{output}")
        try:
            counts[name] = int(match.group(1))
        except ValueError as error:
            raise SystemExit(f"Invalid test count for {name}: {match.group(1)}") from error
    return counts


def loadJson(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise SystemExit(f"Cannot read evidence from {path}: {error}") from error


snapshots = loadJson(ROOT / "snapshots.json")
records = {
    record["label"]: record
    for path in sorted((ROOT / "evidence").glob("*.json"))
    for record in [loadJson(path)]
}
require(len(records) == 35, "Expected all 35 recorded command boundaries")
for digest, files in snapshots.items():
    actual = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    require(actual == digest, f"Source snapshot hash mismatch: {digest}")
for record in records.values():
    require(record["actualExit"] == record["expectedExit"], f"Unexpected recorded exit: {record['label']}")
    for side in ("before", "after"):
        require(record[side]["sourceSha256"] in snapshots, f"Missing source: {record['label']}")


def source(label, side="before"):
    return snapshots[records[label][side]["sourceSha256"]]


# A RED phase may change its test, but not production; GREEN preserves the RED test.
for prior, red, green, testPath in (
    ("04-seed-feature", "05-normal-red", "06-normal-green", "test/shipping-policy.test.mjs"),
    ("11-ambiguity-stop", "12-discount-red", "13-discount-green", "test/checkout-contract.test.mjs"),
    ("28-change-preflight", "29-change-red", "30-change-green", "test/shipping-policy.test.mjs"),
):
    previous = source(prior, "after")
    redSource = source(red)
    changed = {name for name in previous.keys() | redSource.keys() if previous.get(name) != redSource.get(name)}
    require(changed == {testPath}, f"RED changed more than its behavior test: {red}")
    require(records[red]["actualExit"] == 1, f"RED did not fail: {red}")
    for name in redSource:
        if name.startswith("test/"):
            require(redSource[name] == source(green)[name], f"GREEN changed a test: {green}")
    require(records[green]["actualExit"] == 0, f"GREEN did not pass: {green}")

require(source("10-normal-push", "after") == source("11-ambiguity-stop", "after"), "Ambiguity pause changed source")
require(records["11-ambiguity-stop"]["after"]["status"] == "", "Ambiguity pause was not clean")
require(records["24-sync-rebase"]["actualExit"] == 0, "Integration did not complete")
require(records["24-sync-rebase"]["after"]["status"] == "", "Integration was not clean")
require(records["25-sync-required-check"]["actualExit"] == 1, "Inherited sync gate did not fail")
require(records["22-sync-remote-before"]["stdout"] == records["26-sync-remote-after"]["stdout"], "Blocked case changed remote feature ref")
require(not any(r["cwd"] == "sync-case" and r["command"][:2] == ["git", "push"] for r in records.values()), "Recorded push occurred in blocked case")
require(source("17-discount-push", "after") == source("28-change-preflight"), "Requirement-change case used the wrong baseline")
for name in ("shipping.mjs", "checkout.mjs", "amounts.mjs"):
    require(source("31-change-refactor-checks")[name] == source("32-change-feature-checks")[name], "Feature evaluation changed production")

# This replays application behavior from captured source, not an LLM's decisions.
node = shutil.which("node")
if node is None:
    raise SystemExit("Node.js is required to replay the captured fixture")
expectedOutcomes = {
    "01-baseline-tests": (2, 2, 0),
    "05-normal-red": (3, 2, 1),
    "06-normal-green": (3, 3, 0),
    "07-normal-refactor-checks": (3, 3, 0),
    "12-discount-red": (4, 3, 1),
    "13-discount-green": (4, 4, 0),
    "14-discount-refactor-checks": (4, 4, 0),
    "18-upstream-tests": (2, 2, 0),
    "25-sync-required-check": (4, 2, 2),
    "29-change-red": (4, 3, 1),
    "30-change-green": (4, 4, 0),
    "31-change-refactor-checks": (4, 4, 0),
    "32-change-feature-checks": (6, 6, 0),
}
for label, expected in expectedOutcomes.items():
    record = records[label]
    require(record["command"] == ["node", "--test"], f"Unexpected test command: {label}")
    require(record["before"]["sourceSha256"] == record["after"]["sourceSha256"], f"Test run mutated source: {label}")
    with tempfile.TemporaryDirectory(prefix="shipping-replay-") as directory:
        temporary = Path(directory).resolve()
        for name, content in source(label).items():
            target = (temporary / name).resolve()
            require(target.is_relative_to(temporary), f"Unsafe snapshot path: {name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        result = subprocess.run([node, "--test"], cwd=temporary, capture_output=True, text=True)
    require(result.returncode == record["actualExit"], f"Replay exit differs: {label}\n{result.stdout}\n{result.stderr}")
    recordedCounts = testCounts(record["stdout"] + record["stderr"])
    replayedCounts = testCounts(result.stdout + result.stderr)
    requiredCounts = dict(zip(("tests", "pass", "fail"), expected, strict=True))
    require(recordedCounts == requiredCounts, f"Unexpected recorded behavior: {label}")
    require(replayedCounts == requiredCounts, f"Unexpected replayed behavior: {label}")
    print(f"PASS {label}: {requiredCounts}")
print("PASS: source integrity, recorded progression boundaries, and all 13 test-state replays")
