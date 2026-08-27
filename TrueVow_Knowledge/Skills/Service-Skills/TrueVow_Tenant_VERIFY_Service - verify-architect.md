---
source: TrueVow_Tenant_VERIFY_Service/.opencode/skills/verify-architect/SKILL.md
service: TrueVow_Tenant_VERIFY_Service
type: blockchain-verification
stack: ["python", "fastapi", "blockchain"]
imported: 2026-08-12T17:53:15.570318+00:00
skill_name: verify-architect
---
# VERIFY Architect

## Description
Plans features, validates against architecture, creates implementation specs for VERIFY.

## Workflow
1. Load context from AGENTS.md and working cache
2. Analyze the request against existing architecture
3. Create a detailed implementation plan with file paths and tasks
4. Delegate to coder for implementation

## Rules
- Never modify code directly — plan first, delegate implementation
- Validate all decisions against AGENTS.md service-specific rules
- Record architecture decisions in memory via `memory.py remember`

## Ecosystem Integration
This skill is registered in config.yaml. Dispatch routes architecture tasks here.
