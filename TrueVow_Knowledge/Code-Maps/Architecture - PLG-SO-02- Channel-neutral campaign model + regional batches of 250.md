---
category: architecture
title: "PLG-SO-02: Channel-neutral campaign model + regional batches of 250"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T20:52:56.608988+00:00
updated: 2026-08-03T20:52:56.608988+00:00
memory_id: b54e7525-ec88-4a7d-b26e-f3d8d630b22b
---

# PLG-SO-02: Channel-neutral campaign model + regional batches of 250

Migration 181 extends existing campaign tables (no parallel tables). Four concepts separated: campaign programs, audience batches (≤250), enrollments, delivery chunks. Channel adapters: Email active (wraps Resend), SMS/SOCIAL/PAID_MEDIA disabled (CHANNEL_NOT_ENABLED). RegionPartitionFactory with deterministic STATE_FIRST partitioning. Existing email campaigns preserved via table extension.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
