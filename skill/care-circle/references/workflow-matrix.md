# Care circle workflow matrix

Per-step delegation map for the care brief. Every step passes only the real result of the previous step. Read-only steps may continue while a write is pending approval.

| Step | Agent | CLI and action | Effect | Approval | Empty or partial result |
|---|---|---|---|---|---|
| 1 | orchestrator | confirm folder, parent name, appointment date | none | none | missing item returns `waiting_user`; ask once and stop |
| 2 | file-agent | `ug-filesystem find`, `ug-filesystem ls`, `ug-filemgr scan-dedupe` | read | none | empty folder is reported as empty; stop, never broaden the scope |
| 3 | photo-agent | `ug-photo vision-ocr` (one call per image), `ug-photo vision-vlm` | read | none | unreadable label is listed as unreadable; the step still completes |
| 4 | document-agent | `ug-document metadata`, `ug-document page-count`, `ug-document extract` with `file` set to the document paths, schema `medical-report` and an explicit `query` — diagnoses (context only, never published), medications with dates, results and measurements, findings | read | none | no document paths: do not call `ug-document extract`; record no documents and continue. A report that yields no rows is reported as no rows |
| 5 | document-agent | `ug-document qa` intent `comparison` (label vs report, label rows carried in the query), then `ug-document reconcile` over the report paths (report vs earlier report) | read | none | no document paths returns an explicit no documents and no previous report; a medication with no report entry is reported as having no report entry; a single report returns an explicit no previous report; none is resolved by guess |
| 6 | knowledge-agent | `ug-knowledge audio-transcription` with no `language` parameter (the required inputs collect none; the catalog parameter is optional) — transcript and any questions the speaker asked | read | none | a memo with no speech is reported as no transcript; the brief marks the memo as missing |
| 7 | orchestrator | assemble the brief and the sibling update from the real results of steps 2 to 6 | none | none | a section with no source is empty and named as empty |
| 8 | orchestrator | approval gate: present the brief and the sibling update — the medication table, the changes since the visit, the recent results, the questions for the doctor, every label-versus-report conflict, and the unreadable list | none | waiting_approval | no approval means no write; a conflict row is immutable and may be marked unresolved, never removed; a conflict left unresolved stays in the brief marked unresolved |
| 9 | file-agent | `ug-filesystem mkdir` — a packet subfolder inside the care folder returned in step 2, named for the appointment date | state-change | gateway | pending creation is surfaced; read-only work continues |
| 10 | knowledge-agent | two `ug-knowledge save-text` calls, one per document | state-change | workflow | pending write is surfaced; neither document is reported as saved until `completed` |
| 11 | file-agent | `ug-filemgr tag-get-by-name` for the exact names `care-medication`, `care-question`, `care-visit`, passing each as `name` (read, none), `ug-filemgr tag-add` for any name not found (`tag-id` set to the exact tag name; gateway), then `ug-filemgr tag-get-by-name` again for that name (read, none), `ug-filemgr tag-add-file` (`tag-id` set to the identifier returned by `tag-get-by-name`, not the tag name; `path` set to every image and document from step 2 for `care-medication`, every audio file from step 2 for `care-question`, and every file from step 2 for `care-visit`; conditional) | read + state-change | none + gateway + conditional | a tag that cannot be created is reported as unavailable; no file is tagged by guess |
| 12 | orchestrator | report the brief path, the sibling update path, the tagged source files, the conflicts left unresolved, and the unreadable and missing list | none | none | an empty result is reported as empty and the run continues; the run stops only when the care folder itself is empty or a required input is missing |

## Artifact structure

Two dated documents are written to the packet folder.

The care brief is the clinician-facing document, with these sections, in this order:

1. Header: parent name, appointment date, and the folder the brief was built from.
2. Current medications: one row per medication with drug, dose, frequency, the source file it came from, and the label-versus-report status of agree, conflict, or no report entry.
3. Recent results: findings and measurements with their source file.
4. Changes since the previous visit: the `ug-document reconcile` result between the earliest and the most recent report, or an explicit statement that no previous report exists.
5. Questions for the doctor: the open questions the family raised, each with their source.
6. Unreadable and missing list: every file that could not be read, and every expected item that was absent.
7. Confirmation line: a clinician must confirm every entry before it is relied on.

The sibling update is a separate five-line note a sibling can read in under a minute and paste into a family chat.

Diagnoses read in step 4 are context for the comparisons only. No brief section publishes them.

## Delegation state handling

- `completed`: the step result is real and may be passed downstream.
- `failed`: stop every dependent step, preserve partial results, report the step, the file and the reason.
- `cancelled`: the user stopped the run; report what was already written and start no further writes.
- `waiting_user`: a decision is required; ask exactly the missing question, and stop.
- `waiting_approval`: a write, tag, folder creation or the brief itself is pending confirmation; state the pending change, do not repeat it and do not work around it.

## Safety rules

- The skill organises and surfaces only. It never diagnoses and never advises on dosage.
- Every claim carries a source path. A claim with no source is omitted, not guessed.
- A medication row is published only after the label-versus-report comparison is shown to the user and the brief is approved.
- A label-versus-report conflict is reported, never resolved by the skill.
- A conflict row is immutable: the user may mark it unresolved, never remove it.
- Diagnoses read from the source documents are context for the comparisons only; no brief section publishes them.
- A file that could not be read stays on the unreadable list; it is never summarised from memory.
- Writes, tags and folder creation are always approval-gated and are never repeated or bypassed.
- The scope is the folder the user named. The skill never widens it and never substitutes a similar folder.
