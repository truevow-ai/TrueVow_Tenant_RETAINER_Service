---
category: todo
title: "Phase 5: Remaining ungoverned pipeline_stage writes"
importance: 5
tags: []
file_paths: []
created: 2026-08-03T19:36:22.784335+00:00
updated: 2026-08-03T19:36:22.784335+00:00
memory_id: bbb02a0e-05f7-486d-97f6-95e5b4af253b
---

# Phase 5: Remaining ungoverned pipeline_stage writes

26+ legacy pipeline_stage write sites identified. Most go through leadsRepo.update() which auto-translates. Remaining direct supabaseAdmin writes: lead-promotion-service (waitlist path unmapped), test-call-service.ts, demos/request/route.ts, demos/book-discovery/route.ts (lead create). Also onboarding/route.ts and multi-channel-sequence-service.ts now fixed this session.

---
**Category:** `todo` | **Importance:** 5/10
**Files:** N/A
