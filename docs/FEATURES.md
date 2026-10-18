# Feature inventory

Snapshot at case wrap-up: October 17, 2026. “Implemented” refers to code behavior, not validation with older adults in everyday use.

| Feature | Behavior and boundary | Main implementation |
|---|---|---|
| Family setup | Sample family profile, relationships, timezone and sharing acknowledgement. Role selection is not identity verification. | `family/demo.py`, `family/web.py` |
| Conversational intake | Text and attachments stay in one conversation; OpenAI asks follow-ups and returns structured proposed changes. | `family/intelligence.py`, `family/static/app.js` |
| Photos | Model-assisted description, retained original and source note. Picture interpretation still needs review. | `family/resources.py`, `family/intelligence.py` |
| Documents | TXT, Markdown, DOCX and text PDF parsing; scanned-PDF interpretation requires OpenAI. Files up to 10 MB; PDFs up to 60 pages. | `family/resources.py` |
| Public URLs | HTTP/HTTPS retrieval and text extraction; private-network destinations are rejected. No general web-search engine or browser automation. | `family/resources.py` |
| Microphone intake | Browser recording is submitted for transcription, then used in the conversation. Live microphone UX was not reverified during wrap-up. | `family/web.py`, `family/intelligence.py` |
| Confirmed handover | Applies record edits and reviewed attachment notes in one transaction. Rejects stale versions and deduplicates confirmed operations. | `family/web.py`, `family/store.py` |
| Asset library | Original material and reviewed notes remain accessible beneath the conversation. | `family/static/app.js`, resource routes |
| Inbound voice | Guava establishes a role, conducts the live conversation and routes requests to backend callbacks. | `family/phone.py`, `main.py` |
| Context lookup | Fresh structured records, tasks, recent family responses and ranked reviewed-source excerpts. No vector store. | `family/store.py: context` |
| Phone updates | Collects necessary fields, confirms a structured change and saves it through code. Elder-role updates have a smaller allowed category set. | `family/phone.py` |
| Family requests | Explicit request becomes a dashboard issue; multiple occurrences can be grouped by topic. It does not automatically call a family member. | `family/phone.py`, `family/store.py` |
| Calls and outcomes | Speech events persist in messages; a post-call summary records the outcome. Explicit requests survive summarization. | `family/phone.py` |
| Family response | Ownership, status and response notes. Resolving an issue requires a note; responses are included in subsequent context. | `family/web.py`, `family/store.py` |
| Dashboard reminders | Persistent scheduled jobs, cancellation and deduplication. Displaying a reminder does not mean it was read. | `family/worker.py` |
| Outbound phone reminders | Existing worker can call one configured test recipient when explicitly scheduled and phone mode is active. End-to-end outbound delivery remains unverified. | `family/worker.py`, `main.py` |
| Parcel exercise | Simulated transitions and pickup-reminder deduplication. No carrier API, live tracking or verified delivery feed. | `family/store.py`, parcel routes |
| Fresh demo preparation | Reconstructs the fictional Roku case in an empty directory without model calls or live call history. | `scripts/prepare_demo.py` |

## Not implemented as product features

Multi-household tenancy, authenticated accounts, invitation delivery, Apple Watch/HealthKit, actual device control, live carrier tracking, emergency escalation, reliable continuous monitoring, cloud deployment and production operations.

## Data boundaries

The local `data/` directory contains the actual database, uploads and provider configuration. It is ignored by Git. The preparation script uses only the repository’s fictional household material and attributed photo. Historic screenshots are presentation artifacts, not a fresh live-state check. The early tutorial and initial plan remain reference material, not alternative current entry points.
