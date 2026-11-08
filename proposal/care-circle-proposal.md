# UGREEN Hackathon 2026 on AI NAS — Project Proposal

**Project:** care-circle
**Track:** Automate Your Workflow
**Round 1 submission**

---

## 1. What it does

care-circle turns one folder of medication photos, clinic letters and voice memos into a dated, source-cited brief reporting every disagreement between the family's own documents, and a sibling update, computed on the NAS.

## 2. User and problem

Adult children caring for an ageing parent. Evidence is scattered across pill-bottle photos, discharge summaries and unplayed voice memos, so appointments are a scramble.

## 3. Solution

A local care brief that reads each modality with the matching UGOS expert and writes two documents: a source-cited brief covering current medications, label-versus-report conflicts, results, changes since the last visit, questions for the doctor and an unreadable list; and a five-line sibling update. It never diagnoses or advises dosage.

## 4. User flow

The user names a folder, the parent and the appointment date. The file expert enumerates and deduplicates the folder, the photo expert reads medication labels, the document expert extracts clinic letters and compares each medication against its label, and the knowledge expert transcribes voice memos. The brief and sibling update are approved, written back and tagged.

## 5. Difference from existing tools

Existing tools read one source and trust it. care-circle compares them: each medication is read from its label and from the clinic letter, and a disagreement is reported with both sources and left for the clinician. Nothing is reconciled silently, and nothing leaves the NAS.

## 6. NAS capabilities by step

Step 2: `ug-filesystem find` and `ls`, `ug-filemgr scan-dedupe` (file-agent). Step 3: `ug-photo vision-ocr` and `vision-vlm` (photo-agent). Steps 4-5: `ug-document metadata`, `page-count`, `extract` schema `medical-report`, `qa` intent `comparison`, `reconcile` (document-agent). Step 6: `ug-knowledge audio-transcription` (knowledge-agent). Step 9: `ug-filesystem mkdir`. Step 10: `ug-knowledge save-text`. Step 11: `ug-filemgr tag-get-by-name`, `tag-add`, `tag-add-file`.

## 7. Technical approach

Pure Markdown orchestration. It delegates only through `delegate --target` to the four registered experts, passing each step's real result downstream. The comparisons are separate `ug-document qa` and `reconcile` calls, not a single summary. Read steps are ungated; the brief, folder, writes and tags are approval-gated. Inputs: the folder, the parent, the date. The NAS local model performs vision, extraction and transcription; nothing leaves the device.

## 8. Status

Implemented: the twelve-step orchestration, the unreadable list, approval handling, and a static checker pass with zero errors and warnings. Pending NAS validation: both comparisons, on-device vision, extraction, transcription, tag creation and write approval.

## 9. Validation

Core case 1: three medication photos, one letter and one voice memo produce a brief with every claim cited and every unreadable file listed. Core case 2: a second letter produces the change comparison, with one engineered dose disagreement left unresolved. Edge case: one blurry photo and no documents completes with an empty medication section and an unreadable entry.

## 10. Limitations

Vision reading of curved or reflective labels can fail; unreadable labels are reported, never guessed. A label-versus-letter disagreement is surfaced, never resolved by the Skill. Tag creation needs gateway approval. No runtime third-party dependencies; the development tool is the Uliya skill kit.

---

## Team and consent

Entrant: Philip Jon Ji Ciuca (individual entry). All members consent to the official rules and confirm the Skill and its core workflow were developed during the hackathon. No previously developed Skill or submission material is reused.

## Third-party components

The Skill has no runtime third-party dependencies. The Uliya Skill Creation Tool (uliya-skill-kit v0.7.3) was used at development time only and is not distributed inside the Skill package.
