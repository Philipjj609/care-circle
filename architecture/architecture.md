# care-circle — Architecture

**Status:** built, static-pass. **Track:** Automate Your Workflow.
**Round 1 deliverable:** proposal PDF + Skill ZIP.

## 1. Problem and hypothesis

Adult children caring for an ageing parent cannot answer two questions at appointment
time: *what is happening with dad this week?* and *what do I tell the doctor?* The
evidence exists — pill-bottle photos, discharge summaries, voice memos — but it is
scattered across modalities and never assembled.

**Hypothesis:** the winning entry is not the most novel mechanism but the most
demonstrable composition. A judge must see a real folder go in and a real, checkable
artifact come out in the first 30 seconds on a fresh NAS. care-circle is built around
that single moment.

## 2. System shape

Pure Markdown orchestration. One orchestrator (the Skill) and four registered UGOS
expert agents. No scripts, no direct `cli.invoke`, no external services.

```
                    ┌─────────────────────────────┐
                    │        SKILL.md             │
                    │   orchestrator (no CLI)     │
                    └──────────────┬──────────────┘
       ┌───────────────┬───────────┼───────────────┬──────────────┐
       ▼               ▼           ▼               ▼              ▼
  file-agent     photo-agent  document-agent  knowledge-agent   (user)
  ug-filesystem  ug-photo     ug-document     ug-knowledge      approval
  ug-filemgr                               (audio)            gates
```

The orchestrator never reads a file itself. It confirms inputs, delegates, assembles
from real results, and holds the approval gate.

## 3. Workflow (12 steps)

| # | Agent | Action | Effect | Approval |
|---|---|---|---|---|
| 1 | orchestrator | confirm folder, parent name, appointment date | — | none |
| 2 | file-agent | `ug-filesystem find`, `ls`; `ug-filemgr scan-dedupe` | read | none |
| 3 | photo-agent | `ug-photo vision-ocr` (one call per image); `vision-vlm` on ambiguous labels | read | none |
| 4 | document-agent | `ug-document metadata`, `page-count`, `extract` (schema `medical-report`) — diagnoses, medications with dates, results and measurements, findings | read | none |
| 5 | document-agent | `ug-document qa` (intent `comparison`) — label vs report, then report vs earlier report | read | none |
| 6 | knowledge-agent | `ug-knowledge audio-transcription` — transcript and any questions the speaker asked | read | none |
| 7 | orchestrator | assemble the brief and the sibling update from real results 2–6 | — | none |
| 8 | orchestrator | **approval gate** — present brief, conflicts, unreadable list | — | waiting_approval |
| 9 | file-agent | `ug-filesystem mkdir` (packet folder) | state-change | gateway |
| 10 | knowledge-agent | two `ug-knowledge save-text` calls (brief, sibling update) | state-change | workflow |
| 11 | file-agent | `ug-filemgr tag-get-by-name`, `tag-add`, `tag-add-file` | state-change | gateway + conditional |
| 12 | orchestrator | report paths, tags, conflicts, unreadable list | — | none |

**Design rule:** every step passes only the real result of the previous step. A step
that did not run contributes nothing; a value no delegated result contains is never
invented.

## 4. Delegation contract

Each `delegate --target <agent> --instruction '<task>'` is self-contained and states:

- **Scope** — the exact paths or rows returned by the named upstream step.
- **Constraints** — what the agent must not do (not read contents, not widen scope).
- **Negative conditions** — "do not infer a dose that is not written".
- **Output contract** — one row per item with the source path, plus an explicit
  unreadable / not-found mark.
- **Real-result passing** — the instruction names the step whose result it consumes.

## 5. Approval and permission model

| Operation | CLI | Approval | Handling |
|---|---|---|---|
| Folder creation | `ug-filesystem mkdir` | gateway | surfaced; read-only work continues |
| Brief write | `ug-knowledge save-text` | workflow | not reported saved until `completed` |
| Tag creation | `ug-filemgr tag-add` | gateway | requested only when `tag-get-by-name` misses |
| Tag application | `ug-filemgr tag-add-file` | conditional | one tag per resolved identifier |
| Brief approval | orchestrator gate | waiting_approval | **no approval, no write** |

The Skill never repeats a pending change, never works around a gate, and never reports
a write that has not returned `completed`.

## 6. State handling

- `completed` → pass the real result downstream.
- `failed` → stop every dependent step; preserve and list partial results; report the
  step, the file and the reason.
- `cancelled` → report what was already written; start no further writes.
- `waiting_user` → ask exactly the missing question; stop.
- `waiting_approval` → state the pending change; do not repeat or bypass it.

Empty results are reported as empty. The Skill never substitutes a similar folder,
broadens the filter, or fills a gap from memory.

## 7. The artifacts

Two dated documents are written to the packet folder.

The **care brief** is the clinician-facing document, with seven sections in order:

1. Header — parent, appointment date, source folder.
2. Current medications — drug, dose, frequency, source file, label-vs-report status.
3. Recent results — findings and measurements with source.
4. Changes since the previous visit — or an explicit "no previous report".
5. Questions for the doctor — each with its source.
6. Unreadable and missing list.
7. Confirmation line — a clinician must confirm every entry.

The **sibling update** is a separate five-line note a sibling can read in under a
minute and paste into a family chat.

The sibling update is the emotional hook; the unreadable list is the trust hook; the
confirmation line is the safety hook.

## 8. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Pill label unreadable (curved/reflective) | listed as unreadable, never guessed; `vision-vlm` requires an explicit "unreadable" answer |
| Local model weak on vision | finalist pre-tests one label; leads with the document+audio path if weak |
| No previous report | stated as "no baseline"; no comparison invented |
| Label and report disagree | surfaced as a conflict row with both source paths; never auto-resolved |
| Tags absent on a fresh NAS | `tag-get-by-name` → `tag-add` bootstrap (added after council review) |
| Empty folder | reported empty; the run stops rather than widening scope |
| Write approval denied | brief is not reported saved; partial results are preserved |

## 9. Privacy and compliance

All processing is on-device. Medication photos, clinic letters and voice memos are read
by registered UGOS experts; no health data is uploaded and the Skill contains no code
path that could upload it. No credentials, tokens or personal data are collected.
Third-party components: none at runtime. Development-time only: the UGREEN Uliya skill
kit v0.7.3 (not distributed inside the package).

## 10. Verification

- **Static:** `node vendor/uliya-skill-kit/scripts/check-skill.mjs skill/care-circle`
  → `static-pass`, 0 errors, 0 warnings, 0 info, against catalog v2.0.0.
- **Catalog conformance:** all 16 CLI actions used are present in catalog v2.0.0 with
  the stated approval levels.
- **Planned runtime cases (Round 2):**
  - Core 1 — three medication photos + one letter + one memo → brief with every claim
    cited and every unreadable file listed.
  - Core 2 — second run with an added earlier letter → correct "changes since last visit".
  - Edge — one blurry photo and no documents → empty medication section, explicit
    unreadable entry, nothing invented.

## 11. Round 2 demo plan (3 minutes)

| Time | Beat |
|---|---|
| 0:00 | Fresh NAS, nothing pre-loaded. Finalist uploads the care folder (3 label photos, 1 letter, 1 memo, 1 deliberately blurry photo) and names folder, parent, date. |
| 0:30 | File enumeration + `vision-ocr`/`vision-vlm`. Medication table on screen, each row with its source path. |
| 1:00 | Document extraction + label-vs-report comparison flags a dose conflict; voice memo transcribed. |
| 2:00 | Approval gate → packet folder → brief saved → sources tagged. File tree shows the tagged sources. |
| 2:45 | Sibling update read aloud; unreadable list and confirmation line held on screen. End card. |

**Finalist prep:** curate 4–6 files; include a previous-visit report for the baseline;
engineer one deliberate label/report dose conflict; pre-test one label with
`vision-vlm`; pre-create the three tags or rely on the bootstrap.

## 12. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Fresh-NAS vision model returns "unreadable" for all labels | High | honest unreadable list is a designed outcome; demo still shows the artifact and the conflict path via documents |
| Judges see it as "just a summary" | Medium | the artifact is a saved, tagged file set with source paths, not prose |
| Medical liability perception | Medium | never diagnoses, never advises dosage, always prints the clinician-confirmation line |
| Tag bootstrap fails on device | Low | fallback reports tags unavailable; no file is tagged by guess |

## 13. Change log

- 2026-11-08 — council selected care-circle; step 11 amended to bootstrap tags
  (`tag-get-by-name` → `tag-add` → `tag-add-file`); approval gate and
  label-vs-report conflict step added; static re-check green.
- 2026-11-08 — catalog re-audit of every parameter used: `vision-ocr.path` is
  single-valued, so step 3 now runs one call per image; `tag-add` takes `tag-id`,
  so step 11 sets `tag-id` to the tag name; the sibling update is now a separate
  document written by its own `save-text` call, resolving the duplicate-section
  inconsistency in the brief structure.
- 2026-11-08 — claims-vs-does audit against the brief's seven sections: step 4 now
  asks for results and measurements (section 3 had no supporting extraction);
  step 5 now also compares the most recent report against the earlier report
  (section 4, "changes since the previous visit", was claimed but never computed);
  step 6 now returns the questions the speaker asked (section 5).
