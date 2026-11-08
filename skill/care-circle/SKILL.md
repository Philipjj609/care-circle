---
name: care-circle
description: Care circle brief for an ageing parent: reads the medication photos, clinic letters and voice memos stored on the NAS and reports every place two of the family's own documents disagree — a pill bottle against a clinic letter, or one clinic letter against an earlier one — naming both source paths and leaving the disagreement for the clinician. Use when the user asks for a care brief, a medication list, a doctor visit summary, or a family update about a parent.
---

# Goal

Turn one folder of mixed care documents, medication photos and voice memos into a dated, source-cited care brief that a family can hand to a clinician and share with siblings. Every claim in the brief names the file it came from, and every file that could not be read is listed as unreadable. The brief reports every disagreement between two of the family's own documents — each medication read from its label and from the clinic letter, and each medication read from the current letter and from the earlier one — and leaves every disagreement for the clinician. The brief organises and surfaces information only. It never diagnoses, never advises on dosage, and always ends with an instruction that a clinician must confirm every entry.

# Required input

Collect the care folder the user names, the parent's name, and the appointment date. Resolve the folder with `file-workflow get-user-dir` when the user names no path. Do not pre-collect medication names, diagnoses or account values; the registered experts resolve the real files. If the folder, the parent's name or the appointment date is missing, ask for the missing item and stop.

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
- `ug-photo` → `photo-agent`

# Orchestration

1. Confirm the care folder, the parent's name and the appointment date. Keep the scope exactly as named; never widen it.
2. Delegate to file-agent: `delegate --target file-agent --instruction 'Use ug-filesystem find with the user-named care folder and ug-filesystem ls to enumerate every file, returning real paths grouped as documents, images and audio. Then use ug-filemgr scan-dedupe on the same folder and return the duplicate groups. Do not read file contents.'`
3. Delegate to photo-agent: `delegate --target photo-agent --instruction 'Run one ug-photo vision-ocr call per image path returned in step 2; vision-ocr takes a single path, so never pass a list. For any image whose text is missing or ambiguous, run one ug-photo vision-vlm call for that image with a prompt that asks for the drug name, dose, frequency and warnings, and that requires the answer unreadable when the label cannot be read. Return one row per image with drug, dose, frequency, warnings, readability and the source path. Do not infer a dose that is not written.'`
4. Delegate to document-agent: `delegate --target document-agent --instruction 'Use ug-document metadata and ug-document page-count on the document paths returned in step 2, then ug-document extract with schema medical-report to return diagnoses, medications with their dates, results and measurements, findings and the reporting doctor, each row carrying its source file. Do not infer a value that is not written.'`
5. Delegate to document-agent: `delegate --target document-agent --instruction 'Use ug-document qa with intent comparison on the report paths returned in step 2, carrying the medication rows returned in step 3 in the query, stating for each medication whether the label and the report agree, conflict, or have no report entry. Then use ug-document reconcile over the report paths only, asking which medications were added, stopped or changed dose between the earliest and the most recent report; when only one report is present, return an explicit no previous report. Return every agreement, conflict and change with both source paths. Do not resolve a conflict and do not infer a value that is not written.'`
6. Delegate to knowledge-agent: `delegate --target knowledge-agent --instruction 'Use ug-knowledge audio-transcription on the audio paths returned in step 2 with the language the user stated, returning the transcript text, any questions the speaker asked, and the source file for each memo. Do not guess missing audio.'`
7. Assemble the brief and the sibling update from the real results of steps 2 to 6. The brief carries current medications with their source files, the label-versus-report agreement or conflict for each medication, the changes against the earlier report, recent results, questions for the doctor, and an unreadable list. The sibling update is five lines a sibling can read in under a minute. Mark every claim with its source path. Never add a medication, diagnosis or date that no delegated result contains.
8. Approval gate: present the assembled brief and the sibling update to the user and wait, showing the medication table, every label-versus-report conflict, and the unreadable list. Proceed only on explicit user approval of the brief; the user may correct or remove rows. A conflict the user does not resolve stays in the brief marked as unresolved.
9. Delegate to file-agent: `delegate --target file-agent --instruction 'Use ug-filesystem mkdir to create the care packet folder for the appointment date stated by the user, returning the real folder path. Do not create any other folder.'`
10. Delegate to knowledge-agent: `delegate --target knowledge-agent --instruction 'Use two ug-knowledge save-text calls, one for the approved care brief and one for the sibling update, each passing its own content and a filename hint, writing to the real packet folder path returned in step 9. Return the real output paths only.'`
11. Delegate to file-agent: `delegate --target file-agent --instruction 'Use ug-filemgr tag-get-by-name for each of the medication, question and visit tag names. For any name that returns no tag, use ug-filemgr tag-add with tag-id set to that name to create it. Then use ug-filemgr tag-add-file with the tag identifier returned by the lookup, not the tag name. Do not tag any file that was not returned by step 2.'`
12. Report the brief path, the sibling update path, the tagged source files, the conflicts left unresolved, and the unreadable and missing list. If any step returned an empty result, say so plainly and stop; do not substitute a similar folder or broaden the filter.

Pass only the real result of the upstream delegation to the next step. See the [workflow matrix](references/workflow-matrix.md) for the per-step agent, CLI, action and approval map, and the [disclosure and compliance](references/disclosure-and-compliance.md) note for third-party components and data handling.

# Completion and failure

Only report a business result after the delegated expert returns `completed`. A delegation returning `failed` stops every dependent step and reports the step, the file and the reason; partial results are preserved and listed. A delegation returning `cancelled` means the user stopped the run: report what was already written and start no further writes. A delegation returning `waiting_user` means a decision is required: ask exactly the missing question and stop. A delegation returning `waiting_approval` means a write, tag, folder creation or the brief itself is pending user confirmation: state the pending change, do not repeat it, and do not work around it; read-only analysis may continue. An empty result is reported as empty; the skill never substitutes a similar document or expands the search on its own. The brief always prints that a clinician must confirm every entry.
