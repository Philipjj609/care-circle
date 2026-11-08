# Devpost upload — one screen

Everything needed to file the Round 1 submission. Two files, ten answers, one
track. The upload itself needs Philip's Devpost account.

**Deadline:** 15 November 2026, 11:45pm PT.

## The two files

| File | Path | Size | Limit |
|---|---|---|---|
| Project Proposal PDF | `proposal/care-circle-proposal.pdf` | 7,945 bytes, 2 pages | ≤ 1 MB |
| Pre-test Skill Package ZIP | `submission/care-circle-skill.zip` | 6,979 bytes, 3 files | ≤ 10 MB, ≤ 100 files, ≤ 1 MB each |

Both are the canonical copies, byte-identical to `dist/` in the working folder.
The build runs in the working folder, then the copies land here. Re-verify before
uploading:

```bash
cd C:/Users/phili/Desktop/Projects/ugreen-hackathon-work
python3 tools/make_submission.py
cp dist/care-circle-proposal.pdf C:/Users/phili/Desktop/Projects/ugreen-hackathon/proposal/care-circle-proposal.pdf
cp dist/care-circle-pretest-skill.zip C:/Users/phili/Desktop/Projects/ugreen-hackathon/submission/care-circle-skill.zip
```

## Track

**Automate Your Workflow.** The prizes are awarded overall, not per track; the
track only labels the entry. This track's own mission text — "organize content,
extract information, generate summaries, and automate repetitive tasks" — is
care-circle exactly. The 2026-11-08 council split 4-1 in favour of keeping it;
the dissent preferred Open Innovation so the label would match the
differentiation claim.

## The ten answers

Paste each into the matching form field. 457 words in the answers, 489 as the
PDF renders them; the limit is 500.

**1. One sentence: What does the Skill do?**

> care-circle turns one folder of medication photos, clinic letters and voice
> memos into a dated, source-cited brief reporting every disagreement between
> the family's own documents, and a sibling update, computed on the NAS.

**2. Who is the target user and problem?**

> Adult children caring for an ageing parent. Evidence is scattered across
> pill-bottle photos, discharge summaries and unplayed voice memos, so
> appointments are a scramble.

**3. What is your proposed solution?**

> A local care brief that reads each modality with the matching UGOS expert and
> writes two documents: a source-cited brief covering current medications,
> label-versus-report conflicts, results, changes since the last visit,
> questions for the doctor and an unreadable list; and a five-line sibling
> update. It never diagnoses or advises dosage.

**4. What is the Core User Flow?**

> The user names a folder, the parent and the appointment date. The file expert
> enumerates and deduplicates the folder, the photo expert reads medication
> labels, the document expert extracts clinic letters and compares each
> medication against its label, and the knowledge expert transcribes voice
> memos. The brief and sibling update are approved, written back and tagged.

**5. What substantive difference does your idea offer compared with existing
tools or conventional AI solutions?**

> care-circle compares the family's own documents: each medication is read from
> its label and from the clinic letter, and a disagreement is reported with both
> source paths, deliberately left unresolved for the clinician. Nothing is
> reconciled silently, and nothing leaves the NAS.

**6. Which UGREEN AI NAS capabilities will be used, and at which step in the
workflow?**

> Step 1: file-workflow get-user-dir (file-agent). Step 2: ug-filesystem find and
> ls, ug-filemgr scan-dedupe (file-agent). Step 3: ug-photo vision-ocr and
> vision-vlm (photo-agent). Steps 4-5: ug-document metadata, page-count, extract
> schema medical-report, qa intent comparison, reconcile (document-agent).
> Step 6: ug-knowledge audio-transcription (knowledge-agent). Step 9: ug-filesystem
> mkdir. Step 10: ug-knowledge save-text. Step 11: ug-filemgr tag-get-by-name,
> tag-add, tag-add-file.

**7. What was your technical approach?**

> Pure Markdown orchestration. It delegates only through delegate --target to four
> of the six registered experts, passing each step's real result downstream. The
> comparisons are separate ug-document qa and reconcile calls, not a single
> summary. Read steps are ungated; the brief, folder, writes and tags are
> approval-gated. Inputs: the folder, the parent, the date. The NAS local model
> performs vision, extraction and transcription; nothing leaves the device.

**8. What is the current development status?**

> Implemented: the twelve-step orchestration, the unreadable list, approval
> handling, and a static checker pass with zero errors and warnings. Pending NAS
> validation: both comparisons, on-device vision, extraction, transcription, tag
> creation and write approval.

**9. What is your final validation plan?**

> Core case: the seven-file oracle — four medication images (one deliberately
> blurry), two clinic letters and one voice memo — produces a brief with every
> claim cited, every unreadable file listed, the change comparison and one
> engineered dose disagreement left unresolved. Edge case: one blurry photo and no
> documents completes with an empty medication section and an unreadable entry.

**10. Are there any known limitations of your Project?**

> Vision reading of curved or reflective labels can fail; unreadable labels are
> reported, never guessed. A label-versus-letter disagreement is surfaced, never
> resolved by the Skill. Tag creation needs gateway approval. No runtime
> third-party dependencies; the development tool is the Uliya skill kit.

## Other form fields

| Field | Value |
|---|---|
| Project name | `care-circle` |
| One-line tagline | Reports every disagreement between a family's own care documents, computed on the NAS |
| Track | Automate Your Workflow |
| Team members | Philip Jon Ji Ciuca (individual entry) |
| Source code URL | https://github.com/Philipjj609/care-circle — public |
| Sponsors/partners | None to disclose. The hackathon sponsor is AMERICA UGREEN LIMITED (rules §2); no financial or preferential support was received (§4) |
| Third-party notice | None at run time. Development-time only, not distributed in the package: Uliya Skill Creation Tool (uliya-skill-kit v0.7.3). Source: UGREEN Skill Developer Package / Starter Kit. Licence: UGREEN developer licence. |

## Consent wording (if the form asks)

> All members consent to the official rules and confirm the Skill and its core
> workflow were developed during the hackathon. No previously developed Skill or
> submission material is reused.

## Before you submit

- [x] Board decisions applied: track, team, GitHub visibility, emphasis; sponsors researched against the official rules.
- [ ] `python3 tools/make_submission.py` run and the two files re-copied.
- [ ] PDF opens, is 2 pages, and shows no markdown artifacts.
- [ ] ZIP opens and contains `care-circle/SKILL.md` plus the two references.
- [ ] The submission is filed before 15 November 2026, 11:45pm PT.
