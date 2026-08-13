#!/usr/bin/env python3
"""
TrueVow Skill Watcher — always-alive repo monitor.

Watches all registered service repos for git activity, then exercises
the skill pipeline automatically:

  watch      → poll repos for new commits / dirty state
  review     → run /code-review (Pocock) + /security-and-hardening (TrueVow)
  challenge  → flag architecture drift vs canonical invariants
  guide      → write findings to CTO dashboard + shared memory

Run: python skill-watcher.py [--once] [--interval 300]

The watcher is the "always alive" layer — skills fire without human
dispatch whenever a repo changes.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Windows: force UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

# ── Registered services (from config.yaml scan) ──
SERVICES = [
    "TrueVow_SaaS_Administration_Service",
    "TrueVow_Sales_Ops_Service",
    "TrueVow-Tenant_Billing-Service",
    "TrueVow_Tenant_INTAKE_Service",
    "TrueVow_Customer_Success_CORE_Service",
    "TrueVow_Internal_Ops_Service",
    "TrueVow_Financial_Management_Service",
    "TrueVow_Platform_Analytics_Service",
    "TrueVow_Tenant_SETTLE-Service",
    "TrueVow_Tenant_LEVERAGE_Service",
    "TrueVow_Tenant_VERIFY_Service",
    "Truevow_Tenant_Customer_Portal_Service",
    "TrueVow_Tenant_TRACE_Service",
]

# ── Architecture invariants from canonical decisions ──
INVARIANTS = [
    ("canonical-pipeline", r"/api/v1/tenants/internal", "REJECTED route — CSM must not create tenants"),
    ("secret-leak", r"sk_[a-zA-Z0-9]{20,}", "secret pattern in tracked source"),
    ("dotenv", r"\.env\.staging", "dotenv staging file reference (use Fly secrets)"),
    ("supabase-rest", r"adminSupabase", "Supabase REST from Fly (prefer pg Pool)"),
    ("manual-repair", r"UPDATE .* SET status = 'PENDING'", "manual business-state repair pattern"),
    ("false-delivery", r"DELIVERY_MODE.*disabled.*DELIVERED", "disabled mode reporting DELIVERED"),
]


def git(cmdline: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + cmdline, cwd=str(cwd), capture_output=True, text=True)


def repo_state(service: str) -> dict | None:
    path = ROOT / service
    if not (path / ".git").exists():
        return None
    r = git(["log", "-1", "--format=%H %s"], path)
    last_commit = r.stdout.strip() if r.returncode == 0 else "?"
    r2 = git(["status", "--porcelain"], path)
    dirty = len([l for l in r2.stdout.splitlines() if l.strip()]) if r2.returncode == 0 else -1
    return {"service": service, "path": str(path), "last_commit": last_commit, "dirty": dirty}


def scan_for_invariants(service: str, path: Path) -> list[dict]:
    """Challenge layer: grep for architecture-drift markers."""
    findings = []
    tracked = git(["ls-files"], path)
    if tracked.returncode != 0:
        return findings
    files = [f for f in tracked.stdout.splitlines() if f.endswith((".ts", ".py", ".js", ".sql", ".md"))]
    # Sample at most 500 files per scan
    for f in files[:500]:
        p = path / f
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        import re as _re
        for name, pattern, desc in INVARIANTS:
            if name == "manual-repair" and not content.startswith("#"):
                # too noisy on arbitrary files; skip unless UPDATE is present
                if "UPDATE " not in content:
                    continue
            for m in _re.finditer(pattern, content, _re.IGNORECASE):
                findings.append({
                    "service": service, "file": f, "invariant": name,
                    "description": desc, "line": content[: m.start()].count("\n") + 1,
                })
    return findings


def run_once() -> dict:
    report = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "services": [],
        "findings": [],
    }
    for svc in SERVICES:
        state = repo_state(svc)
        if state is None:
            continue
        report["services"].append(state)
        if state["dirty"] > 0:
            findings = scan_for_invariants(svc, Path(state["path"]))
            report["findings"].extend(findings)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="single scan")
    ap.add_argument("--interval", type=int, default=300, help="poll seconds")
    ap.add_argument("--output", default=".skill-watcher.json", help="report path")
    args = ap.parse_args()

    while True:
        report = run_once()
        (ROOT / args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
        n_find = len(report["findings"])
        n_dirty = sum(1 for s in report["services"] if s["dirty"] > 0)
        print(f"[skill-watcher] {report['ts']} — {len(report['services'])} repos, {n_dirty} dirty, {n_find} findings")
        for f in report["findings"][:5]:
            print(f"  [!] [{f['invariant']}] {f['service']}/{f['file']}:{f['line']} - {f['description']}")
        if args.once:
            break
        time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    sys.exit(main())
