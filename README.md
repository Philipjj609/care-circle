# care-circle — UGREEN Hackathon 2026 on AI NAS

Round 1 submission for the UGREEN Hackathon 2026 on AI NAS (Devpost).
**Track:** Automate Your Workflow. **Entrant:** Philip Jon Ji Ciuca (individual).

care-circle reads one folder of medication photos, clinic letters and voice
memos and reports every disagreement between the family's own documents — a pill
bottle against a clinic letter, or one clinic letter against an earlier one —
naming both sources and leaving the disagreement for the clinician. It is pure
Markdown orchestration over UGOS expert agents — no scripts, no external
services, no data leaves the device.

## What is in this repository

This is the submission repository. It holds only what a judge needs.

```
skill/care-circle/                 the Uliya Skill package
  SKILL.md                         entry point (required)
  references/workflow-matrix.md    per-step agent / CLI / approval map
  references/disclosure-and-compliance.md
proposal/care-circle-proposal.md  the ten proposal answers
proposal/care-circle-proposal.pdf the submitted PDF (<= 1 MB)
submission/care-circle-skill.zip  the submitted ZIP (<= 10 MB, 3 files)
submission/devpost-upload.md      the one-screen Devpost upload guide
```

Round 2 material (final package, demo video) is added here if care-circle is
shortlisted as a finalist. Internal working notes, council records, competitor
research and the build tooling are kept in a separate private project folder and
are deliberately not part of this repository.

## Build the deliverables

```bash
python3 tools/make_submission.py
# -> dist/care-circle-proposal.pdf and dist/care-circle-pretest-skill.zip
#    also enforces the 500-word proposal limit and prints both counts
```

Then sync the canonical copies, or the submitted files drift from the build:

```bash
cp dist/care-circle-proposal.pdf proposal/care-circle-proposal.pdf
cp dist/care-circle-pretest-skill.zip submission/care-circle-skill.zip
```

## Check the Skill

Requires Node and the UGREEN Uliya skill kit v0.7.3.

```bash
node <uliya-skill-kit>/scripts/check-skill.mjs skill/care-circle
# -> status: static-pass, errors 0, warnings 0 (catalog v2.0.0)
```

## Round 1 status

- Official static checker: **static-pass**, 0 errors, 0 warnings, 0 info.
- Proposal: 455 English words in the ten answers; 487 including the section
  headings, so it stays under the 500-word limit on the strictest reading.
- Package: 3 files, 6,371 bytes compressed, 15,040 bytes uncompressed.
- Not yet validated: the label-versus-report and report-versus-report
  comparisons, and the on-device behaviour of `ug-photo vision-ocr`/`vision-vlm`,
  `ug-document extract` (schema `medical-report`), `ug-document reconcile`,
  `ug-knowledge audio-transcription`, tag creation and write approval. These are
  Round 2 items.

## Round 2 (finalists)

Invited Nov 21; one day of remote NAS access Nov 22–28; final package and a
three-minute YouTube video due Nov 30. Round 1 scores do not carry over —
winners are decided by Round 2 only.

## Entrant

Philip Jon Ji Ciuca (individual entry). The Skill and its core workflow were
developed during the hackathon; no previously developed Skill or submission
material is reused. No third-party components are used at run time; the Uliya
skill kit v0.7.3 was used at development time only and is not distributed in the
package.
