#!/usr/bin/env python3
"""
TrueVow Skill Gate — pre-commit / pre-push hook.

Exercises the skill pipeline automatically on every commit:
  1. SECURITY: skillspector scan (if installed) + TrueVow secret patterns
  2. REVIEW:   diff-based review using /code-review + /security-and-hardening rules
  3. GATE:     blocks commit on CRITICAL findings

Install: python skill-gate.py --install <repo-path>
Run:     python skill-gate.py            (from a service repo)
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Windows: force UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

# ── TrueVow security rules (from /security-and-hardening skill) ──

SECRET_PATTERNS = [
    (r"sk_live_[a-zA-Z0-9]+", "CRITICAL", "Stripe live key"),
    (r"sk-ant-[a-zA-Z0-9-]{20,}", "CRITICAL", "Anthropic API key"),
    (r"AIza[0-9A-Za-z_-]{30,}", "CRITICAL", "Google API key"),
    (r"xai-[a-zA-Z0-9]{20,}", "CRITICAL", "xAI API key"),
    (r"AKIA[0-9A-Z]{16}", "CRITICAL", "AWS access key"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL", "Private key material"),
    (r"ghp_[a-zA-Z0-9]{30,}", "CRITICAL", "GitHub personal access token"),
    (r"postgresql://[^:\s]+:[^@\s]+@", "HIGH", "Database URL with credentials"),
    (r"password\s*[:=]\s*['\"][^'\"]+['\"]", "HIGH", "Hardcoded password"),
    (r"secret\s*[:=]\s*['\"][^'\"]{8,}['\"]", "HIGH", "Hardcoded secret"),
]

# Files to never scan
SKIP_GLOBS = {"*.lock", "package-lock.json", "pnpm-lock.yaml", "*.map", "*.min.js", "*.pyc", ".env.example"}

# Files to always skip (generated)
SKIP_DIRS = {".next", "node_modules", "__pycache__", ".git", "dist", "build", ".venv"}


def get_staged_files() -> list[str]:
    r = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return [f.strip() for f in r.stdout.splitlines() if f.strip()]


def should_skip(path: str) -> bool:
    p = Path(path)
    if any(part in SKIP_DIRS for part in p.parts):
        return True
    if p.suffix and f"*{p.suffix}" in SKIP_GLOBS:
        return True
    if p.name in SKIP_GLOBS:
        return True
    return False


def scan_secrets(files: list[str]) -> list[dict]:
    findings = []
    for f in files:
        if should_skip(f):
            continue
        try:
            content = Path(f).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern, severity, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, content):
                line_no = content[: m.start()].count("\n") + 1
                findings.append({
                    "file": f, "line": line_no, "severity": severity,
                    "rule": f"secret: {label}", "evidence": m.group(0)[:40],
                })
    return findings


def scan_markers(files: list[str]) -> list[dict]:
    """TrueVow-specific invariant markers from /security-and-hardening."""
    findings = []
    TODO_CRITICAL = re.compile(r"TODO.*(?:FIXME|XXX|HACK|TEMP|HOTFIX)", re.IGNORECASE)
    for f in files:
        if should_skip(f):
            continue
        try:
            content = Path(f).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in TODO_CRITICAL.finditer(content):
            line_no = content[: m.start()].count("\n") + 1
            findings.append({
                "file": f, "line": line_no, "severity": "LOW",
                "rule": "review: dangerous TODO marker", "evidence": m.group(0)[:60],
            })
    return findings


def run_skillspector(files: list[str]) -> list[dict]:
    """Run SkillSpector if installed."""
    findings = []
    for f in files:
        if should_skip(f):
            continue
        r = subprocess.run(
            ["skillspector", "scan", f, "--no-llm"],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode == 0 and r.stdout:
            findings.append({"file": f, "line": 0, "severity": "INFO",
                             "rule": "skillspector", "evidence": r.stdout.strip()[:200]})
    return findings


def gate(findings: list[dict]) -> tuple[bool, int, int, int]:
    critical = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high = sum(1 for f in findings if f["severity"] == "HIGH")
    other = len(findings) - critical - high
    return (critical == 0 and high == 0), critical, high, other


def main() -> int:
    hook = sys.argv[1] if len(sys.argv) > 1 else "pre-commit"

    if hook == "--install":
        target = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
        hooks_dir = target / ".git" / "hooks"
        if not hooks_dir.exists():
            print(f"Not a git repo: {target}")
            return 1
        src = Path(__file__).resolve()
        for name in ("pre-commit",):
            dest = hooks_dir / name
            script = f"#!/bin/sh\npython \"{src}\" pre-commit \"$@\"\n"
            dest.write_text(script)
            dest.chmod(0o755)
        print(f"✓ Skill gate installed in {target}")
        return 0

    files = get_staged_files()
    if not files:
        print("✓ SKILL GATE: nothing staged")
        return 0

    print(f"→ SKILL GATE: reviewing {len(files)} staged file(s)")

    findings = []
    findings += scan_secrets(files)
    findings += scan_markers(files)
    findings += run_skillspector(files)

    passed, critical, high, other = gate(findings)

    for f in findings:
        sev = f["severity"]
        icon = {"CRITICAL": "⛔", "HIGH": "⚠️", "LOW": "ℹ️", "INFO": "✓"}.get(sev, "·")
        print(f"  {icon} [{sev}] {f['rule']}: {f['file']}:{f['line']} — {f['evidence']}")

    if passed:
        print(f"✓ SKILL GATE PASS: {len(files)} files clean ({other} advisory)")
        return 0
    else:
        print(f"\n⛔ SKILL GATE BLOCKED: {critical} CRITICAL, {high} HIGH")
        print("  Fix CRITICAL/HIGH findings or run with --force for emergency bypass.")
        print("  Skills applied: /security-and-hardening (TrueVow), /code-review (Pocock)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
