# TrueVow Agent Ecosystem

> **Skills are the new apps.** Harness-agnostic. Pure files + CLI. Works with any coding agent.
> **Multi-developer.** Shared memory via git-tracked memory.db. All 4 devs sync one CTO brain.

## START HERE — the CTO Second Brain

**Before anything else, read [`TrueVow_Context/START-HERE.md`](TrueVow_Context/START-HERE.md).** It is the portable, tool-agnostic context any agent or developer is pointed at first — what TrueVow is, the service + trust-domain map, the binding decisions, and the voice/standards. Point any AI at `TrueVow_Context/` and it becomes the TrueVow CTO's second brain; no re-explaining the platform every session.

## Multi-Developer Setup (First Time)

```bash
git clone --recursive <truevow-cto-agent-repo-url>
cd Cursor
set TRUEVOW_DEV=your-name    # Windows
export TRUEVOW_DEV=your-name  # Mac/Linux
```

## Multi-Developer Daily Workflow

### Start of Session — Pull Shared Knowledge
```
python TrueVow_Shared_Orchestration/orchestrator.py sync-memory
```
This pulls the latest memory.db from git. Every developer's decisions are now visible to you.

### During Work — Remember Decisions
```
python TrueVow_Shared_Orchestration/memory.py remember <category> "<title>" "<content>" --importance N
```
This auto-stages memory.db for git. Your `TRUEVOW_DEV` name is attached to every entry.

### End of Session — Push Your Knowledge
```
python TrueVow_Shared_Orchestration/orchestrator.py push-memory
```
This commits and pushes memory.db. Other developers will see your decisions on their next `sync-memory`.

### Full Session Workflow
```
sync-memory → dispatch "<task>" → work → remember → push-memory → sync-obsidian
```

## Developer Identity

Set your identity so the CTO knows who stored what:
```
set TRUEVOW_DEV=yasha         # Yasha (Founder)
set TRUEVOW_DEV=sania          # Ms. Sania (Sales Ops)
set TRUEVOW_DEV=ghaus-fsd      # Ghulam Ghaus (Tenant App + Billing)
set TRUEVOW_DEV=ghous-isb      # Ghulam Ghous (SaaS Admin + CSM)
```

## Standard Agent Workflow

When an agent begins work on this codebase, it should:

## 1. Load Context
- Run `python TrueVow_Shared_Orchestration/orchestrator.py sync-memory` to pull shared knowledge from all developers
- Run `python TrueVow_Shared_Orchestration/orchestrator.py memory-summary` to see what the project remembers
- Run `python TrueVow_Shared_Orchestration/orchestrator.py list` to see available skills
- Run `python TrueVow_Shared_Orchestration/orchestrator.py scan-services` to get real-time git state of all 13 services

## 2. Auto-Dispatch: Map Intent → Skill → Persona
**Before doing any work**, the agent must run:
```
python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<user's request>"
```
This auto-maps the user's intent to the right skill + persona and prints the full SKILL.md.
The agent must then **follow the SKILL.md instructions exactly** — never partially.

## 3. Dispatch Table (for quick reference)
| User says... | Skill loaded | Persona activated |
|-------------|-------------|-------------------|
| "review this code" / "PR review" | code-review (Pocock) + security-and-hardening (TrueVow) | code-reviewer |
| "write tests" / "test coverage" | tdd (Pocock) | test-engineer |
| "security audit" / "vulnerability" | security-and-hardening (TrueVow) | security-auditor |
| "performance / slow / optimize" | performance-optimization (TrueVow) | web-performance-auditor |
| "ship / launch / deploy" | shipping-and-launch (TrueVow) | code-reviewer + security-auditor + test-engineer (parallel fan-out) |
| "new feature / spec / define" | to-spec (Pocock) | — |
| "plan / breakdown / tasks" | to-tickets (Pocock) | — |
| "implement / build / develop" | implement (Pocock) → uses tdd internally | — |
| "bug / broken / debug / fix" | diagnosing-bugs (Pocock) + observability-and-instrumentation (TrueVow) | — |
| "simplify / refactor / messy" | improve-codebase-architecture (Pocock) | — |
| "api / endpoint / contract" | api-and-interface-design (TrueVow) → uses to-spec | — |
| "ui / frontend / component" | prototype (Pocock) | — |
| "search web / research / twitter" | research (Pocock) | — |
| "align on idea / grill me" | grill-me (Pocock) | — |
| "handoff to another agent" | handoff (Pocock) | — |
| "route / which skill" | truevow-ask (TrueVow) | — |
| "read source / understand" | source-driven-development (TrueVow) | — |
| "deprecate / migrate" | deprecation-and-migration (TrueVow) → uses to-tickets | — |
| "browser test / devtools" | browser-testing-with-devtools (TrueVow) → uses diagnosing-bugs | — |
| "ci/cd / deploy" | ci-cd-and-automation (TrueVow) | — |
| "setup repo" | setup-matt-pocock-skills (Pocock) | — |

> **Pocock skills** handle engineering fundamentals. **TrueVow skills** add platform-specific knowledge (SigNoz, Fly, Supabase, Clerk, ontology). Both live in `TrueVow_Shared_Agent_Tools/agent-skills/skills/`.

## 4. Remember Everything
After important decisions, architecture changes, bug discoveries:
```
python TrueVow_Shared_Orchestration/memory.py remember <category> "<title>" "<content>" --importance 8
```
Categories: architecture, pattern, decision, dependency, convention, bug, context, todo, relationship

## 5. Push Shared Knowledge
After storing important memories:
```
python TrueVow_Shared_Orchestration/orchestrator.py push-memory
```
This shares your decisions with all other developers via the git-tracked memory.db.

## 6. Work Incrementally
- One thin vertical slice at a time
- RED → GREEN → REFACTOR → COMMIT
- Never skip the test

## 7. Stay Informed — Realtime Git Scan
Every hour during your session, re-run the services scan so you always have current state:
```
python TrueVow_Shared_Orchestration/orchestrator.py scan-services
```
The `doctor` command now includes this automatically.

## 8. Review Before Shipping
- Five-axis review: correctness, readability, architecture, security, performance
- Scan skills before installing: `skillspector scan TrueVow_Shared_Agent_Tools/agent-skills/skills/ --recursive`

## Available Commands
| Command | Purpose |
|---------|---------|
| `python TrueVow_Shared_Orchestration/orchestrator.py sync-memory` | Pull latest shared knowledge from all devs |
| `python TrueVow_Shared_Orchestration/orchestrator.py push-memory` | Push your knowledge to shared repo |
| `python TrueVow_Shared_Orchestration/orchestrator.py doctor` | Full ecosystem diagnostic |
| `python TrueVow_Shared_Orchestration/orchestrator.py list` | List all skills + personas |
| `python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<request>"` | Auto-map intent → skill + load SKILL.md |
| `python TrueVow_Shared_Orchestration/orchestrator.py scan-services` | Realtime git state of all 13 services |
| `python TrueVow_Shared_Orchestration/orchestrator.py dashboard` | View all active developers |
| `python TrueVow_Shared_Orchestration/memory.py summarize` | Memory database summary |
| `python TrueVow_Shared_Orchestration/memory.py remember <cat> <title> <content>` | Store a memory |
| `python TrueVow_Shared_Orchestration/memory.py recall <query>` | Search memories |
| `python TrueVow_Shared_Orchestration/obsidian-bridge.py` | Sync to Obsidian vault |
| `agent-reach doctor` | Check web channel status |
| `skillspector scan <path>` | Security scan a skill |

## All Registered Agents
- **4 Personas:** code-reviewer, test-engineer, security-auditor, web-performance-auditor
- **24 Lifecycle Skills:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP (Pocock fundamentals + TrueVow platform)
- **10 TrueVow Platform Skills:** security-and-hardening, performance-optimization, shipping-and-launch, ci-cd-and-automation, api-and-interface-design, observability-and-instrumentation, source-driven-development, deprecation-and-migration, browser-testing-with-devtools, using-agent-skills
- **25 Pocock Engineering Skills:** ask-matt, tdd, code-review, to-spec, to-tickets, implement, diagnosing-bugs, prototype, research, grill-me, grill-with-docs, handoff, teach, domain-modeling, codebase-design, improve-codebase-architecture, resolving-merge-conflicts, wizard, triage, wayfinder, writing-for-agents, grilling, wait-what, to-questionnaire, setup-matt-pocock-skills
- **2 Tool Skills:** agent-reach (web), skillspector-guardrail (security)
- **4 Developers:** yasha, sania, ghaus-fsd, ghous-isb
- **Sub-repo agents:** agent-skills AGENTS.md, Agent-Reach CLAUDE.md, SkillSpector README

## Obsidian Vault
All knowledge syncs to `TrueVow_Knowledge/`. Run `python TrueVow_Shared_Orchestration/obsidian-bridge.py` to update.
