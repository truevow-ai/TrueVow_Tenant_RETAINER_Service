---
category: decision
title: "TRACE billing LLM switched to DeepSeek API"
importance: 8
tags: []
file_paths: []
created: 2026-07-18T08:24:27.350073+00:00
updated: 2026-07-18T08:24:27.350073+00:00
memory_id: 628ddf2e-abb0-4581-8970-28a7203f84ce
---

# TRACE billing LLM switched to DeepSeek API

Azure denied quota increase for trace-gpt-5.4-mini deployment. Per user decision, LLM_SERVICE_PROVIDER=deepseek_api in .env.local. DeepSeekAPILLMService verified live (deepseek-chat responded OK, usage 10 tokens). CAUTION: DeepSeek public API has NO BAA - PHI-stripping rules mandatory per llm.py docstring; LLM_PHI_ALLOWED must stay false. Azure creds left in .env.local for potential rollback.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
