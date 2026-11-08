# Three Skill concepts for UGREEN AI NAS Hackathon 2026

Persona filter: parent of two young children, caregiver for an ageing parent, freelancer WFH.
All three are demoable on a fresh iDX6011 Pro with documents + photos + audio the finalist brings. No cameras, no media library required.

---

## 1. care-circle

**(a) Name:** `care-circle`

**(b) Pitch:** A private, local care log that turns medication photos, medical reports, and your parent's voice memos into a one-page doctor-ready brief and a weekly sibling update.

**(c) Target user + problem:** Adult children caring for an ageing parent. The problem is not "where is the document" — it is "what is happening with dad this week, and what do I tell the doctor?" The information is scattered across photos of pill bottles, PDF discharge summaries, and voice memos; every appointment is a scramble.

**(d) Workflow (agent + capability at each step):**
1. User names a folder (or `file-workflow get-user-dir`), the parent's name, and optionally the appointment date.
2. `delegate --target file-agent --instruction '...'` — `ug-filesystem find`/`ls` to enumerate the folder; `ug-filemgr scan-dedupe` to drop duplicates.
3. `delegate --target photo-agent --instruction '...'` — `ug-photo vision-ocr` on every medication/symptom photo; `ug-photo vision-vlm` for ambiguous packaging ("read the label: drug, dose, frequency, warnings").
4. `delegate --target document-agent --instruction '...'` — `ug-document extract` with `schema=medical-report` to pull diagnoses, meds, dates, doctor; `ug-document qa` with `intent=comparison` to diff current vs. prior meds.
5. `delegate --target knowledge-agent --instruction '...'` — `ug-knowledge audio-transcription` on the parent's voice memos; `ug-knowledge save-text` to write the brief and the sibling update (write step, approval).
6. `delegate --target file-agent --instruction '...'` — `ug-filemgr tag-add-file` (conditional approval) to tag sources `care/2026-11`, `care/medication`, `care/question`; `ug-filesystem mkdir`/`echo` for the packet folder (approval).
7. States: `completed` -> next step; `failed`/`cancelled` -> preserve partial results, skip dependent steps, report what is missing; `waiting_user` -> ask for the missing path/appointment date; `waiting_approval` -> surface the tag/mkdir/save write and continue with read-only analysis.

**(e) Tangible output:** A dated one-page brief (current meds, recent results, changes since last visit, questions for the doctor, 5-line sibling update), tagged source files, and an explicit "could not read" list.

**(f) Why different from every competitor:** Haven is a static emergency handbook from documents; Where It Is is a document dossier + expiry diffs. Neither reads a pill bottle via OCR/VLM or transcribes the parent, and neither produces a time-boxed appointment brief or a sibling update. family-archive-weaver does audio + photos for memory and story, not care coordination. portrait-consent-guardian does photos + documents + voice for publication consent, not health coordination.

**(g) Biggest risk:** Medical misreading. Mitigation: never diagnose; the skill organizes and surfaces, prints "confirm with a clinician", and keeps an explicit unreadable list. It transcribes label text and does not advise on dosage.

**Score:** User Value 9, Innovation 8, Technical Quality 7, AI NAS Fit 9 = **33/40**

---

## 2. sunday-reset

**(a) Name:** `sunday-reset`

**(b) Pitch:** Every Sunday it scans the week's school notices, bills, medical letters, kids' photos, and voice memos, and hands you a one-page brief: what needs a signature, payment, or decision, what happened, and what to prep next.

**(c) Target user + problem:** Parent of two young children. The problem is the Sunday-night dig through email, WhatsApp, and the camera roll to find the permission slip, the bill, and what the kids actually did this week.

**(d) Workflow (agent + capability at each step):**
1. Ask for the family folder path and the week; `file-workflow get-user-dir` if needed.
2. `delegate --target file-agent --instruction '...'` — `ug-filesystem find` with date range and `type=documents`; `ug-filemgr scan-dedupe`.
3. `delegate --target document-agent --instruction '...'` — `ug-document extract` with `schema=mixed` to pull due dates, amounts, required actions; `ug-document qa` with `intent=condition`/`period` to find deadlines; `ug-document writing` with `task=minutes` to draft the brief (approval).
4. `delegate --target photo-agent --instruction '...'` — `ug-photo search-picture` with `start-time`/`end-time` plus `ocr-contains`/`ai-object-*` filters for kids' photos and photographed notices; `ug-photo vision-ocr` on any paper; `ug-photo create-album` (approval) to file the week.
5. `delegate --target knowledge-agent --instruction '...'` — `ug-knowledge audio-transcription` on voice memos; `ug-knowledge save-text` for the brief (approval).
6. `delegate --target file-agent --instruction '...'` — `ug-filemgr tag-add-file` `action/2026-W45` (conditional approval); `ug-filesystem mkdir`/`echo` for the brief (approval).
7. States: `completed` -> next; `failed`/`cancelled` -> keep partial, skip dependents; `waiting_user` -> ask for missing path/week; `waiting_approval` -> surface the write and continue read-only.

**(e) Tangible output:** A dated brief (This week / Needs you / Next week / Skipped-uncertain), tagged source files, and an optional album of the week's photos.

**(f) Why different from every competitor:** Haven and Where It Is are static inventories and expiry diffs over documents; neither ingests photos or audio, and neither produces a recurring action brief. Craft Back Office is business, not family. No competitor does a recurring cross-modal family brief.

**(g) Biggest risk:** It reads like a chatbot summary, not NAS work. Mitigation: the artifact is a saved, tagged file set with source paths; the demo shows the tag list and the file tree, not just prose. Second risk: deadline extraction from messy scans — always show confidence and the source snippet.

**Score:** User Value 8, Innovation 8, Technical Quality 8, AI NAS Fit 9 = **33/40**

---

## 3. tax-packet

**(a) Name:** `tax-packet`

**(b) Pitch:** Point it at a year of invoices, receipts, contracts, and bank PDFs and it produces a tax packet: income by client, deductions by category, missing receipts, conflicts, and a filing checklist — every number tied to a source file.

**(c) Target user + problem:** Freelancer working from home. The problem is tax time: a year of mixed business/personal files, lost receipts, and no idea what is deductible.

**(d) Workflow (agent + capability at each step):**
1. Ask for the tax year and folder(s); optional business name.
2. `delegate --target file-agent --instruction '...'` — `ug-filesystem find` with `type=documents` and date range; `ug-filemgr scan-dedupe`; `ug-filesystem md5sum`/`sha256sum` to confirm identical files.
3. `delegate --target document-agent --instruction '...'` — `ug-document extract` with `schema=invoice`/`contract`/`expense`/`receipt`/`mixed_reconciliation` to pull dates, amounts, counterparties, tax IDs; `ug-document reconcile` to find duplicates/conflicts; `ug-document qa` with `intent=comparison` to match invoice vs. receipt.
4. `delegate --target photo-agent --instruction '...'` — `ug-photo vision-ocr` on receipt photos; `ug-photo vision-vlm` for crumpled or handwritten receipts.
5. `delegate --target knowledge-agent --instruction '...'` — `ug-knowledge audio-transcription` for the freelancer's expense notes; `ug-knowledge save-text` for the packet (approval).
6. `delegate --target file-agent --instruction '...'` — `ug-filemgr tag-add-file` `income`/`deduction`/`missing` (conditional approval); `ug-filesystem mkdir`/`echo` for the packet folder (approval).
7. States: `completed` -> next; `failed`/`cancelled` -> keep partial, skip dependents; `waiting_user` -> ask for missing year/folder; `waiting_approval` -> surface the write and continue read-only.

**(e) Tangible output:** A packet folder with an income table, a deductions table, a missing-receipts list, a conflicts/duplicates list, and a filing checklist — each row citing the source path.

**(f) Why different from every competitor:** Craft Back Office is ongoing CRM/invoicing/back office; this is year-end close with source-cited reconciliation and a filing checklist, using the extract schemas and `reconcile`. Evidence Ledger does SHA-256 dedupe and cited claims, but for document claims, not money.

**(g) Biggest risk:** Financial accuracy and overlap with Craft Back Office. Mitigation: frame as evidence organizer, not accountant; cite every number; print "verify with your accountant"; do not compute tax owed.

**Score:** User Value 8, Innovation 7, Technical Quality 9, AI NAS Fit 8 = **32/40**

---

## Which one I would actually rely on

`care-circle`. It is the one I would open every week, the one where the cost of missing something is highest, and the one I would least trust to a cloud service. Health data stays on the NAS; that is the point.

## The single most important strategic bet

**Bet on the 30-second artifact, not the architecture.** Round 2 is a 3-minute video on a fresh NAS with data the finalist brings; the winner is the skill that shows a real folder of mixed family files going in and a real, checkable artifact coming out in the first 30 seconds. Build the whole skill around that one moment and make everything else optional. The four judging criteria are equally weighted, but the demo is the only thing they all see: a concept that cannot be shown quickly loses on User Value, Technical Quality, and AI NAS Fit at once. The secondary moat is cross-modal orchestration (documents + photos + audio) — 9 of the 11 public competitors are single-modal.
