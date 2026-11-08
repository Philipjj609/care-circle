# UGREEN Hackathon 2026 on AI NAS — Project Proposal

**Project:** care-circle
**Track:** Automate Your Workflow
**Round 1 submission**

---

## 1. What it does

care-circle turns one folder of medication photos, clinic letters and voice memos into a dated, source-cited doctor-visit brief and a sibling update, computed on the NAS.

## 2. User and problem

Adult children caring for an ageing parent. Evidence is scattered across pill-bottle photos, discharge summaries and unplayed voice memos, so every appointment is a scramble.

## 3. Solution

A local care brief that reads each modality with the matching UGOS expert and writes two documents: a source-cited brief covering current medications with their sources, label-versus-report conflicts, recent results, changes since the last visit, questions for the doctor and an unreadable list; and a five-line sibling update. It never diagnoses or advises dosage.

## 4. User flow

The user names a folder, the parent and the appointment date. The file expert enumerates and deduplicates the folder, the photo expert reads medication labels, the document expert extracts clinic letters and compares each medication against its label, and the knowledge expert transcribes voice memos. The brief and sibling update are approved, written back and tagged at source.

## 5. Difference from existing tools

Existing tools are static inventories, expiry diffs or single-modal cloud assistants. None reads a pill bottle with on-device vision, transcribes the parent's voice, extracts the clinic letter and binds every claim to its source. Health data never leaves the NAS; the brief is written back with sources tagged in place.

## 6. NAS capabilities by step

Step 2: `ug-filesystem find` and `ls`, `ug-filemgr scan-dedupe` (file-agent). Step 3: `ug-photo vision-ocr` and `vision-vlm` (photo-agent). Steps 4-5: `ug-document metadata`, `page-count`, `extract` schema `medical-report`, `qa` intent `comparison` (document-agent). Step 6: `ug-knowledge audio-transcription` (knowledge-agent). Step 9: `ug-filesystem mkdir`. Step 10: `ug-knowledge save-text`. Step 11: `ug-filemgr tag-get-by-name`, `tag-add`, `tag-add-file`.

## 7. Technical approach

Pure Markdown orchestration. It delegates only through `delegate --target` to the four registered experts in order, passing each step's real result downstream. Read steps are ungated; brief approval, folder creation, writes and tags are approval-gated. Inputs: the folder, the parent, the date. The NAS local model performs vision, extraction and transcription; nothing leaves the device.

## 8. Status

Implemented: the twelve-step orchestration, the label-versus-report and change-since-visit comparisons, the unreadable list, approval handling, and a static checker pass with zero errors and warnings. Pending NAS validation: on-device vision, extraction, transcription, tag creation and write approval.

## 9. Validation

Core case 1: three medication photos, one clinic letter and one voice memo produce a brief with every claim cited and every unreadable file listed. Core case 2: a second run with an earlier letter shows the change since the last visit. Edge case: one blurry photo and no documents completes with an empty medication section and an unreadable entry.

## 10. Limitations

Vision reading of curved or reflective labels can fail; unreadable labels are reported, never guessed. Medication detail is only as good as the sources. A conflict is reported, not resolved. Tag creation needs gateway approval. No runtime third-party dependencies; the development tool is the Uliya skill kit.

---

## Team and consent

Entrant: Philip Jon Ji Ciuca (individual entry). All members consent to the official rules and confirm the Skill and its core workflow were developed during the hackathon. No previously developed Skill or submission material is reused.

## Third-party components

The Skill has no runtime third-party dependencies. The Uliya Skill Creation Tool (uliya-skill-kit v0.7.3) was used at development time only and is not distributed inside the Skill package.
