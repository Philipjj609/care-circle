# Care circle workflow matrix

Per-step delegation map for the care brief. Every step passes only the real result of the previous step. Read-only steps may continue while a write is pending approval.

| Step | Agent | CLI and action | Effect | Approval | Empty or partial result |
|---|---|---|---|---|---|
| 1 | orchestrator | confirm folder, parent name, appointment date | none | none | missing item returns `waiting_user`; ask once and stop |
| 2 | file-agent | `ug-filesystem find`, `ug-filesystem ls`, `ug-filemgr scan-dedupe` | read | none | empty folder is reported as empty; stop, never broaden the scope |
| 3 | photo-agent | `ug-photo vision-ocr`, `ug-photo vision-vlm` | read | none | unreadable label is listed as unreadable; the step still completes |
| 4 | document-agent | `ug-document metadata`, `ug-document page-count`, `ug-document extract` schema `medical-report` | read | none | a report that yields no rows is reported as no rows |
| 5 | document-agent | `ug-document qa` intent `comparison` | read | none | a medication with no report entry is reported as having no report entry, never resolved by guess |
| 6 | knowledge-agent | `ug-knowledge audio-transcription` | read | none | a memo with no speech is reported as no transcript; the brief marks the memo as missing |
| 7 | orchestrator | assemble the brief from the real results of steps 2 to 6 | none | none | a section with no source is omitted and named as not available |
| 8 | orchestrator | approval gate: present the brief, the conflicts and the unreadable list | none | waiting_approval | no approval means no write; a conflict left unresolved stays in the brief marked unresolved |
| 9 | file-agent | `ug-filesystem mkdir` | state-change | gateway | pending creation is surfaced; read-only work continues |
| 10 | knowledge-agent | `ug-knowledge save-text` | state-change | workflow | pending write is surfaced; the brief is not reported as saved until `completed` |
| 11 | file-agent | `ug-filemgr tag-get-by-name`, `ug-filemgr tag-add`, `ug-filemgr tag-add-file` | state-change | gateway + conditional | a tag that cannot be created is reported as unavailable; no file is tagged by guess |

## Brief structure

The brief is a single dated document with these sections, in this order:

1. Header: parent name, appointment date, and the folder the brief was built from.
2. Current medications: one row per medication with drug, dose, frequency, the source file it came from, and the label-versus-report status of agree, conflict, or no report entry.
3. Recent results: findings and measurements with their source file.
4. Changes since the previous visit: the comparison result, or an explicit statement that no previous report exists.
5. Questions for the doctor: the open questions the family raised, each with its source.
6. Sibling update: five lines a sibling can read in under a minute.
7. Unreadable and missing list: every file that could not be read, and every expected item that was absent.
8. Confirmation line: a clinician must confirm every entry before it is relied on.

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
- A file that could not be read stays on the unreadable list; it is never summarised from memory.
- Writes, tags and folder creation are always approval-gated and are never repeated or bypassed.
- The scope is the folder the user named. The skill never widens it and never substitutes a similar folder.
