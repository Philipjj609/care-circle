# UGREEN Hackathon 2026 on AI NAS — Project Proposal

**Project:** care-circle
**Track:** Automate Your Workflow
**Round 1 submission**

---

## 1. What it does

care-circle turns one folder of medication photos, clinic letters and voice memos into a dated, source-cited brief reporting every disagreement between the family's own documents, plus a sibling update, computed on the NAS.

## 2. User and problem

Adult children caring for an ageing parent. Evidence is scattered across pill-bottle photos, discharge summaries and unplayed voice memos, so appointments are a scramble.

## 3. Solution

A local care brief that reads each modality with the matching UGOS expert and writes two documents: a source-cited brief covering current medications, label-versus-report conflicts, results, changes since the last visit, questions and an unreadable list; and a five-line sibling update. It never diagnoses or advises dosage.

## 4. User flow

The user names a folder, the parent and the appointment date. The file expert enumerates and deduplicates the folder, the photo expert reads labels, the document expert extracts letters and compares each medication against its label, and the knowledge expert transcribes voice memos. The brief and sibling update are approved, written back and tagged.

## 5. Difference from existing tools

care-circle compares each medication across the label read on-device, the clinic letter and the earlier letter, reporting every disagreement with both source paths, deliberately unresolved. Voice memos become the questions for the doctor; one run also writes a five-line family update. Nothing leaves the NAS.

## 6. NAS capabilities by step

1. `file-workflow get-user-dir` (file-agent). 2. `ug-filesystem find` and `ls`, `ug-filemgr scan-dedupe` (file-agent). 3. `ug-photo vision-ocr` and `vision-vlm` (photo-agent). 4–5. `ug-document metadata`, `page-count`, `extract` schema `medical-report`, `qa` intent `comparison`, `reconcile` (document-agent). 6. `ug-knowledge audio-transcription` (knowledge-agent). 9. `ug-filesystem mkdir`. 10. `ug-knowledge save-text`. 11. `ug-filemgr tag-get-by-name`, `tag-add`, `tag-add-file`.

## 7. Technical approach

Pure Markdown orchestration. It delegates only through `delegate --target` to four of the six registered experts, passing each step's real result downstream. The comparisons are separate `ug-document qa` and `reconcile` calls, not a single summary. Read steps are ungated; the brief, folder, writes and tags are approval-gated. Inputs: the folder, the parent, the date. The NAS local model performs vision, extraction and transcription; nothing leaves the device.

## 8. Status

Implemented: the twelve-step orchestration, the unreadable list, approval handling, and a static checker pass with zero errors. Pending NAS validation: both comparisons, on-device vision, extraction, transcription, tag creation and write approval.

## 9. Validation

Core case one: the seven-file oracle — four medication images (one deliberately blurry), two clinic letters and one voice memo — produces a brief with every claim cited, the change comparison and one engineered dose disagreement unresolved. Core case two: an agreeing label and letter produce no conflict row. Edge case: one blurry photo and no documents yields an empty medication section and an unreadable entry.

## 10. Limitations

Vision reading of curved or reflective labels can fail; unreadable labels are reported, never guessed. A label-versus-letter disagreement is surfaced, never resolved. Tag creation needs gateway approval. No runtime third-party dependencies; the development tool is the Uliya skill kit.

---

## Team and consent

Entrant: Philip Jon Ji Ciuca (individual entry). All members consent to the official rules and confirm the Skill and its core workflow were developed during the hackathon. No previously developed Skill or submission material is reused.

## Third-party components

The Skill has no runtime third-party dependencies. Development-time only, not distributed inside the Skill package: Uliya Skill Creation Tool (uliya-skill-kit v0.7.3). Source: UGREEN Skill Developer Package / Starter Kit. Licence: UGREEN developer licence.
