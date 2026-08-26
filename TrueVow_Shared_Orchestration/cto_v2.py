#!/usr/bin/env python3
"""
CTO Orchestrator v2 — master control layer for the TrueVow platform.
Spec: TrueVow_CTO_Knowledge_Orchestrator/CTO-ORCHESTRATOR-V2-SPEC.md

Commands:
  status          Scan all repos: branch, last commit, dirty-file count
  next            Topological walk of Tickets/ -> READY tickets + blocked-with-why
  board           Regenerate KANBAN-BOARD.md from tickets + live git state
  brief TICKET    Render work-order brief into the target repo (hygiene-frozen repos refused)
  junior REPO TITLE   Generate a bounded junior assignment (scope + acceptance checklist
                      + constraints + review step + integration step) in that repo
  canonical KEY "decision"   Record a canonical fix (Decisions/ + memory) so a solved
                      defect cannot be silently overwritten and reappear
  review ID       Generate the review artifact for a completed work order (gates integration)
  integrate ID    Print the merge + verification plan for a reviewed work order
  junior REPO TITLE   Generate a bounded junior assignment (scope + acceptance checklist
                      + constraints + review step + integration step) in that repo
  canonical KEY "decision"   Record a canonical fix (Decisions/ + memory) so a solved
                      defect cannot be silently overwritten and reappear
  review ID       Generate the review artifact for a completed work order (gates integration)
  integrate ID    Print the merge + verification plan for a reviewed work order
  done TICKET     Mark ticket DONE with a result summary
  report          One-screen founder report (changes since last shift, blockers, asks)
  shift           Full session cycle: status -> board -> next -> report (safe/read-only)

Design rules (binding):
  - Read-only against service repos EXCEPT writing docs/work-orders/<TICKET>.md briefs.
  - Never commits, stashes, discards, or deploys anything itself (hygiene is classified
    by the target repo's agent per its brief; DISCARD requires explicit founder verb).
  - Hard-stop operations are never automated here; they become AWAITING_FOUNDER tickets.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../Cursor
ORCH_REPO = os.path.join(ROOT, "TrueVow_CTO_Knowledge_Orchestrator")
TICKETS_DIR = os.path.join(ORCH_REPO, "Tickets")
BOARD = os.path.join(ORCH_REPO, "KANBAN-BOARD.md")
STATE = os.path.join(ORCH_REPO, ".cto-v2-state.json")

# Canonical repo registry. Corrections overlay config.yaml (which still carries
# pre-rename paths). Extras are repos config.yaml does not register yet (TICKET-004).
SERVICES = {
    "SaaS Admin":        "TrueVow_SaaS_Administration_Service",
    "Sales Ops":         "TrueVow_Sales_Ops_Service",
    "INTAKE":            "TrueVow_Tenant_INTAKE_Service",
    "RETAINER":          "TrueVow_Tenant_RETAINER_Service",
    "TRACE":             "TrueVow_Tenant_TRACE_Service",
    "SETTLE":            "TrueVow_Tenant_SETTLE-Service",
    "Billing":           "TrueVow-Tenant_Billing-Service",
    "COMMAND":           "TrueVow_Tenant_COMMAND_Service",
    "Customer Portal":   "Truevow_Tenant_Customer_Portal_Service",
    "CSM CORE":          "TrueVow_Customer_Success_CORE_Service",
    "First Line Support":"TrueVow_First_Line_Support_Service",
    "Financial Mgmt":    "TrueVow_Financial_Management_Service",
    "Internal Ops":      "TrueVow_Internal_Ops_Service",
    "Platform Analytics":"TrueVow_Platform_Analytics_Service",
    "LEVERAGE":          "TrueVow_Tenant_LEVERAGE_Service",
    "VERIFY":            "TrueVow_Tenant_VERIFY_Service",
    "Website":           "2026_TrueVow_Website",
}

TICKET_STATUSES = ["READY", "IN_PROGRESS", "BLOCKED", "AWAITING_FOUNDER", "DONE", "SHELVED"]


def sh(args, cwd=None):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def scan_repos():
    rows = []
    for name, rel in SERVICES.items():
        path = os.path.join(ROOT, rel)
        if not os.path.isdir(path):
            rows.append({"name": name, "path": rel, "missing": True})
            continue
        if not os.path.exists(os.path.join(path, ".git")):
            rows.append({"name": name, "path": rel, "no_git": True})
            continue
        branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], path) or "?"
        head = sh(["git", "log", "-1", "--pretty=format:%h|%ad|%s", "--date=short"], path) or ""
        sha, _, rest = head.partition("|")
        hdate, _, subj = rest.partition("|")
        dirty_out = sh(["git", "status", "--porcelain"], path) or ""
        dirty = len([l for l in dirty_out.splitlines() if l.strip()])
        rows.append({"name": name, "path": rel, "branch": branch, "sha": sha,
                     "date": hdate, "subject": subj, "dirty": dirty, "missing": False})
    return rows


def load_tickets():
    tickets = []
    if not os.path.isdir(TICKETS_DIR):
        return tickets
    for fn in sorted(os.listdir(TICKETS_DIR)):
        if not re.match(r"TICKET-\d+", fn) or not fn.endswith(".md"):
            continue
        path = os.path.join(TICKETS_DIR, fn)
        text = open(path, encoding="utf-8").read()
        head, _, body = text.partition("\n---\n")
        t = {"file": fn, "path": path}
        for line in head.splitlines():
            m = re.match(r"^(\w+):\s*(.+)$", line.strip())
            if m:
                k, v = m.group(1).lower(), m.group(2).strip()
                if k == "depends_on":
                    t[k] = [d.strip() for d in v.split(",") if d.strip()]
                elif k == "hygiene":
                    t[k] = v.lower() in ("true", "yes", "1")
                else:
                    t[k] = v
        t.setdefault("depends_on", [])
        t.setdefault("hygiene", False)
        t["body"] = body
        tickets.append(t)
    return tickets


def ticket_state(tickets):
    """Compute readiness: READY iff all depends_on are DONE."""
    by_id = {t.get("id"): t for t in tickets}
    for t in tickets:
        deps = t.get("depends_on", [])
        unresolved = []
        for d in deps:
            dt = by_id.get(d)
            if dt is None:
                unresolved.append(f"{d} (unknown)")
            elif dt.get("status") != "DONE":
                unresolved.append(f"{d} ({dt.get('status')})")
        if t.get("status") == "READY" and unresolved:
            t["_effective"] = "BLOCKED"
            t["_why"] = ", ".join(unresolved)
        else:
            t["_effective"] = t.get("status", "READY")
            t["_why"] = ""
    return tickets


def cmd_status():
    rows = scan_repos()
    print(f"{'REPO':<18} {'BRANCH':<28} {'LAST COMMIT':<12} DIRTY")
    print("-" * 78)
    frozen = []
    for r in rows:
        if r.get("missing"):
            print(f"{r['name']:<18} MISSING: {r['path']}")
            continue
        if r.get("no_git"):
            print(f"{r['name']:<18} NO LOCAL GIT - absorbed into root workspace repo!")
            continue
        mark = " <-- FROZEN" if r["dirty"] > 0 else ""
        if r["dirty"] > 0:
            frozen.append(r["name"])
        print(f"{r['name']:<18} {r['branch']:<28} {r['date']:<12} {r['dirty']}{mark}")
    root_branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], ROOT)
    root_dirty = len([l for l in (sh(["git", "status", "--porcelain"], ROOT) or "").splitlines() if l.strip()])
    print(f"{'(root workspace)':<18} {(root_branch or '?'):<28} {'':<12} {root_dirty}")
    if frozen:
        print(f"\nHYGIENE RULE: {len(frozen)} repo(s) frozen for new assignments "
              f"(uncommitted changes): {', '.join(frozen)}")


def cmd_next():
    ts = ticket_state(load_tickets())
    ready = [t for t in ts if t["_effective"] == "READY"]
    other = [t for t in ts if t["_effective"] != "READY" and t["_effective"] != "DONE"]
    print(f"READY ({len(ready)}):")
    for t in ready:
        print(f"  {t.get('id')}  {t.get('title')}  [{t.get('repo')}]")
    if other:
        print(f"\nNOT READY ({len(other)}):")
        for t in other:
            why = f"  waiting on: {t['_why']}" if t["_why"] else ""
            print(f"  {t.get('id')}  [{t['_effective']}]  {t.get('title')}{why}")


def cmd_board():
    ts = ticket_state(load_tickets())
    rows = scan_repos()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cols = {
        "blocked": [t for t in ts if t["_effective"] in ("BLOCKED",)],
        "awaiting": [t for t in ts if t["_effective"] in ("AWAITING_FOUNDER",)],
        "progress": [t for t in ts if t["_effective"] in ("IN_PROGRESS",)],
        "ready": [t for t in ts if t["_effective"] in ("READY",)],
        "done": [t for t in ts if t["_effective"] in ("DONE", "SHELVED")],
    }
    def item(t):
        s = f"- [ ] **{t.get('id')}** {t.get('title')} _[{t.get('repo')}]_"
        if t["_why"]:
            s += f" — waits on {t['_why']}"
        return s
    frozen = ", ".join(r["name"] for r in rows if not r.get("missing") and not r.get("no_git") and r["dirty"] > 0) or "none"
    nogit = ", ".join(r["name"] for r in rows if r.get("no_git")) or "none"
    lines = [
        "---", "kanban-plugin: basic", "---", "",
        f"> Auto-generated by `cto_v2.py board` — {now}. Do not hand-edit; edit Tickets/ instead.",
        "> Hygiene-frozen repos right now: " + frozen,
        "> CRITICAL - no local git: " + nogit, "",
        "## Blocked", "",
    ]
    lines += [item(t) for t in cols["blocked"]] or ["(none)"]
    lines += ["", "## Awaiting Founder", ""]
    lines += [item(t) for t in cols["awaiting"]] or ["(none)"]
    lines += ["", "## In Progress", ""]
    lines += [item(t) for t in cols["progress"]] or ["(none)"]
    lines += ["", "## Ready (unblocked work)", ""]
    lines += [item(t) for t in cols["ready"]] or ["(none)"]
    lines += ["", "## Done", ""]
    lines += [f"- [x] **{t.get('id')}** {t.get('title')}" for t in cols["done"]] or ["(none)"]
    lines += ["", "## Repo Pulse (live git)", "",
              "| Repo | Branch | Last commit | Dirty |", "|---|---|---|---|"]
    for r in rows:
        if r.get("missing"):
            lines.append(f"| {r['name']} | MISSING | {r['path']} | - |")
        elif r.get("no_git"):
            lines.append(f"| {r['name']} | NO LOCAL GIT | absorbed into root repo | - |")
        else:
            lines.append(f"| {r['name']} | {r['branch']} | {r['date']} {r['sha']} | {r['dirty']} |")
    lines.append("")
    open(BOARD, "w", encoding="utf-8").write("\n".join(lines))
    print(f"Board regenerated: {os.path.relpath(BOARD, ROOT)}")


BRIEF_TEMPLATE = """# Work Order {tid} — {title}

> Issued by CTO Orchestrator v2 on {date}. Target repo: **{repo}**. Goal: {goal}.
> Close the loop: end your session report with `TICKET: {tid}` and what was proven.

## Task

{body}

## Constraints (binding)

- RULE 0 — no fabrication. Report only what you directly observed.
- Platform invariants: `TrueVow_Context/2026-08-10-TRUEVOW-DEVELOPER-START-HERE.md` §6.
- Do NOT deploy to production, migrate shared databases, or change secrets — those
  require an AWAITING_FOUNDER ticket first.
- Commit only with a message referencing `{tid}`. Never discard work silently;
  propose DISCARD options and wait for the founder verb.

## Report-back format

1. What was proven (with real vs simulated evidence labeled)
2. Files changed (git status/diff summary)
3. Tests run (counts, pass/fail)
4. Open questions for the founder, if any
"""


def cmd_brief(tid):
    ts = ticket_state(load_tickets())
    t = next((x for x in ts if x.get("id") == tid), None)
    if not t:
        print(f"No ticket {tid}"); sys.exit(1)
    if t["_effective"] != "READY" and t["_effective"] != "IN_PROGRESS":
        print(f"{tid} is {t['_effective']}, not READY. Resolve dependencies first.")
        sys.exit(1)
    repo_rel = SERVICES.get(t.get("repo"))
    repo_path = os.path.join(ROOT, repo_rel) if repo_rel else None
    if not os.path.isdir(repo_path):
        print(f"Unknown/unmapped repo for ticket: {t.get('repo')}"); sys.exit(1)
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"{t.get('repo')} has NO local git (absorbed into root workspace). "
              f"Resolve TICKET-022 before issuing work there."); sys.exit(1)
    dirty = len([l for l in (sh(["git", "status", "--porcelain"], repo_path) or "").splitlines() if l.strip()])
    if dirty > 0 and not t.get("hygiene"):
        print(f"HYGIENE FREEZE: {t.get('repo')} has {dirty} uncommitted changes.\n"
              f"New assignments refused until changes are COMMIT/PARK/DISCARD-classified.\n"
              f"If this task IS the classification, set 'hygiene: true' in the ticket header.")
        sys.exit(1)
    wodir = os.path.join(repo_path, "docs", "work-orders")
    os.makedirs(wodir, exist_ok=True)
    dest = os.path.join(wodir, f"{tid}.md")
    open(dest, "w", encoding="utf-8").write(BRIEF_TEMPLATE.format(
        tid=tid, title=t.get("title"), date=datetime.now(timezone.utc).date().isoformat(),
        repo=t.get("repo"), goal=t.get("goal", "-"),
        body=(t.get("body") or "").strip()))
    # flip ticket to IN_PROGRESS
    text = open(t["path"], encoding="utf-8").read()
    text = re.sub(r"^status:\s*\w+", f"status: IN_PROGRESS\ngenerated: {dest}", text, count=1, flags=re.M)
    open(t["path"], "w", encoding="utf-8").write(text)
    print(f"Brief written: {dest}\nTicket {tid} -> IN_PROGRESS")


def cmd_done(tid, summary=""):
    ts = load_tickets()
    t = next((x for x in ts if x.get("id") == tid), None)
    if not t:
        print(f"No ticket {tid}"); sys.exit(1)
    today = datetime.now(timezone.utc).date().isoformat()
    text = open(t["path"], encoding="utf-8").read()
    text = re.sub(r"^status:\s*\w+", "status: DONE", text, count=1, flags=re.M)
    text += f"\n## Result ({today})\n\n{summary}\n"
    open(t["path"], "w", encoding="utf-8").write(text)
    print(f"{tid} -> DONE. Remember to record it:")
    print(f'  python TrueVow_Shared_Orchestration/memory.py remember context "{tid} done" "<summary>" --importance 6')


def cmd_report():
    state = {}
    if os.path.exists(STATE):
        state = json.load(open(STATE, encoding="utf-8"))
    prev = state.get("heads", {})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"CFO-SHIFT REPORT — {now}")
    print("=" * 60)
    rows = scan_repos()
    changed = [r for r in rows if not r.get("missing") and not r.get("no_git")
               and r["sha"] and prev.get(r["name"]) not in (None, r["sha"])]
    moved = [r for r in rows if not r.get("missing") and not r.get("no_git")
             and r["sha"] and prev.get(r["name"]) is None]
    if prev and not changed:
        print("Repo changes since last shift: none")
    elif changed or moved:
        print("Repo activity since last shift:")
        for r in changed:
            print(f"  {r['name']}: {r['date']} {r['sha']} {r['subject'][:60]}")
    ts = ticket_state(load_tickets())
    ready = [t for t in ts if t["_effective"] == "READY"]
    await_ = [t for t in ts if t["_effective"] == "AWAITING_FOUNDER"]
    prog = [t for t in ts if t["_effective"] == "IN_PROGRESS"]
    blocked = [t for t in ts if t["_effective"] == "BLOCKED"]
    print(f"\nTickets: {len(ready)} ready | {len(prog)} in progress | "
          f"{len(blocked)} blocked | {len(await_)} awaiting YOU")
    for t in await_:
        print(f"  NEEDS YOU: {t.get('id')} {t.get('title')}")
    frozen = [r["name"] for r in rows if not r.get("missing") and not r.get("no_git") and r["dirty"] > 0]
    nogit = [r["name"] for r in rows if r.get("no_git")]
    if frozen:
        print(f"\nHygiene flags (frozen): {', '.join(frozen)}")
        print("  -> issue hygiene briefs: cto_v2.py brief TICKET-00x")
    if nogit:
        print(f"\nCRITICAL - no local git: {', '.join(nogit)}  (see TICKET-022)")
    # save heads
    state["heads"] = {r["name"]: r["sha"] for r in rows
                      if not r.get("missing") and not r.get("no_git") and r["sha"]}
    state["last_report"] = now
    json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1)
    print(f"\nState saved. Next shift will diff against these HEADs.")


# ---------------- junior layer ----------------

JUNIOR_TEMPLATE = """# Junior Assignment @@JID@@ - @@TITLE@@

> Repo: **@@REPO@@** - issued @@DATE@@ - bounded, review-gated, integration-gated.
> You are a junior developer. Do NOT decide scope, architecture, or what ships.
> This document defines exactly what you may touch and what "done" means.
> Before coding, read canonical fixes for this repo in
> TrueVow_CTO_Knowledge_Orchestrator/Decisions/Canonical-*.md - never re-solve a
> solved defect or overwrite an existing fix without citing why it is superseded.

## Scope (only these)

- [ ] (fill 2-3 concrete items you own)
- [ ] Nothing outside this list without asking first.

## Definition of Done (all must be true)

- [ ] Code committed with a message referencing @@JID@@
- [ ] Repo truth commands pass (lint/typecheck/tests)
- [ ] No secrets, PHI, or raw stack traces introduced
- [ ] Report-back section below completed honestly

## Constraints (binding)

- RULE 0 - no fabrication. Report only what you directly observed.
- NO deploys, NO migrations on shared data, NO secret changes (founder gate).
- Ambiguity => STOP and ask. Never guess-and-proceed.
- Cross-service files are off-limits unless the assignment names them.

## Report-back

1. What I did:
2. Evidence observed (real vs simulated labeled):
3. Tests run + results:
4. Questions for reviewer/founder:
"""

def cmd_junior(repo, title):
    """Bounded junior assignment written into <repo>/docs/work-orders/."""
    repo_rel = SERVICES.get(repo)
    repo_path = os.path.join(ROOT, repo_rel) if repo_rel else None
    if not repo_path or not os.path.isdir(repo_path):
        print(f"Unknown repo: {repo}"); sys.exit(1)
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"{repo} has NO local git - resolve TICKET-022 first."); sys.exit(1)
    dirty = len([l for l in (sh(["git", "status", "--porcelain"], repo_path) or "").splitlines() if l.strip()])
    if dirty > 0:
        print(f"HYGIENE FREEZE: {repo} has {dirty} uncommitted changes. "
              f"Run hygiene classification first."); sys.exit(1)
    jdir = os.path.join(repo_path, "docs", "work-orders")
    os.makedirs(jdir, exist_ok=True)
    n = 1 + len([f for f in os.listdir(jdir) if f.startswith("JUNIOR-")])
    jid = f"JUNIOR-{n:03d}"
    content = (JUNIOR_TEMPLATE
               .replace("@@JID@@", jid)
               .replace("@@REPO@@", repo)
               .replace("@@TITLE@@", title or "(untitled)")
               .replace("@@DATE@@", datetime.now(timezone.utc).date().isoformat()))
    open(os.path.join(jdir, jid + ".md"), "w", encoding="utf-8").write(content)
    print(f"Junior assignment written: {os.path.join(repo_rel, 'docs', 'work-orders', jid + '.md')}")
    print(f"When they finish:  cto_v2.py review {jid}   ->   cto_v2.py integrate {jid}")

def cmd_canonical(key, decision):
    """Record a canonical fix so a solved defect cannot be silently overwritten."""
    dec_dir = os.path.join(ORCH_REPO, "Decisions")
    os.makedirs(dec_dir, exist_ok=True)
    slug = (re.sub(r"[^a-z0-9]+", "-", (key or "").lower()).strip("-") or "fix")[:60]
    today = datetime.now(timezone.utc).date().isoformat()
    path = os.path.join(dec_dir, f"Canonical-{slug}.md")
    body = (decision or "").strip() or "(empty)"
    if os.path.exists(path):
        text = open(path, encoding="utf-8").read()
        text += "\n\n## Update (" + today + ")\n\n" + body + "\n"
    else:
        text = ("# Canonical Fix - " + slug + "\n\n> Recorded " + today +
                ". Authoritative resolution for defect key `" + key + "`.\n"
                "> Later agents MUST NOT overwrite this fix; supersede only with a new\n"
                "> dated entry explaining why.\n\n"
                "## Defect key\n\n`" + key + "`\n\n"
                "## Canonical decision\n\n" + body + "\n")
    open(path, "w", encoding="utf-8").write(text)
    print(f"Canonical recorded: {os.path.relpath(path, ROOT)}")
    print("Now persist to shared memory:")
    print(f'  python TrueVow_Shared_Orchestration/memory.py remember decision '
          f'"Canonical: {key}" "<summary>" --importance 8')

REVIEW_TEMPLATE = """# Review - @@JID@@ (@@REPO@@)

> Generated @@DATE@@. Integration is GATED on this review being APPROVED.

@@WORK_ORDER@@

## Review checklist

- [ ] Scope respected (nothing outside the assignment changed)
- [ ] Truth commands green (paste outputs)
- [ ] No secrets/PHI; no stack traces to browser
- [ ] Cross-service ownership respected
- [ ] Commits reference @@JID@@

## Verdict

- [ ] APPROVED  ->  then run: cto_v2.py integrate @@JID@@
- [ ] REJECTED  ->  blockers listed above; do not integrate
"""

def cmd_review(jid):
    """Generate the review artifact for a completed work order."""
    found = None
    for name, rel in SERVICES.items():
        p = os.path.join(ROOT, rel, "docs", "work-orders", jid + ".md")
        if os.path.exists(p):
            found = (name, p); break
    if not found:
        print(f"No work order {jid} in any repo docs/work-orders/"); sys.exit(1)
    repo, wpath = found
    rdir = os.path.join(ORCH_REPO, "Reviews")
    os.makedirs(rdir, exist_ok=True)
    rpath = os.path.join(rdir, jid + ".md")
    content = (REVIEW_TEMPLATE
               .replace("@@JID@@", jid)
               .replace("@@REPO@@", repo)
               .replace("@@DATE@@", datetime.now(timezone.utc).date().isoformat())
               .replace("@@WORK_ORDER@@", open(wpath, encoding="utf-8").read()))
    open(rpath, "w", encoding="utf-8").write(content)
    print(f"Review artifact: {os.path.relpath(rpath, ROOT)}")
    print("Checklist APPROVED unlocks: cto_v2.py integrate " + jid)

def cmd_integrate(jid):
    """Print the merge + verification plan; gated on APPROVED review."""
    rpath = os.path.join(ORCH_REPO, "Reviews", jid + ".md")
    if not os.path.exists(rpath):
        print(f"No review for {jid} - integration gated. Run: cto_v2.py review {jid}")
        sys.exit(1)
    if "[x] APPROVED" not in open(rpath, encoding="utf-8").read():
        print(f"Review {jid} is not APPROVED - integration blocked."); sys.exit(1)
    print(f"INTEGRATION PLAN {jid}")
    print("=" * 60)
    print("1. Target branch clean; pull latest.")
    print("2. Re-run repo truth commands on the branch (lint/typecheck/tests).")
    print("3. Merge with a commit message referencing " + jid + "; push.")
    print("4. Record the outcome:")
    print(f'   python TrueVow_Shared_Orchestration/memory.py remember context "{jid} integrated" "<what shipped>" --importance 6')
    print("5. Anything regresses afterwards: STOP, open a ticket. NEVER force-merge.")


def cmd_shift():
    cmd_status()
    print()
    cmd_board()
    print()
    cmd_next()
    print()
    cmd_report()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "shift"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    summary = sys.argv[3] if len(sys.argv) > 3 else ""
    if cmd == "status":  cmd_status()
    elif cmd == "next":  cmd_next()
    elif cmd == "board": cmd_board()
    elif cmd == "brief": cmd_brief(arg)
    elif cmd == "done":  cmd_done(arg, summary)
    elif cmd == "report":cmd_report()
    elif cmd == "junior": cmd_junior(arg, summary)
    elif cmd == "canonical": cmd_canonical(arg, summary)
    elif cmd == "review": cmd_review(arg)
    elif cmd == "integrate": cmd_integrate(arg)
    elif cmd == "shift": cmd_shift()
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
