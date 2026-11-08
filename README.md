# care-circle — UGREEN Hackathon 2026 on AI NAS

Round 1 submission for the UGREEN Hackathon 2026 on AI NAS (Devpost).
**Track:** Automate Your Workflow.

care-circle reads one folder of medication photos, clinic letters and voice
memos and reports every disagreement between the family's own documents — a pill
bottle against a clinic letter, or one clinic letter against an earlier one —
naming both sources and leaving the disagreement for the clinician. It is pure
Markdown orchestration over UGOS expert agents — no scripts, no external
services, no data leaves the device.

## Repository layout

```
skill/care-circle/                 the Uliya Skill package
  SKILL.md                         entry point (required)
  references/workflow-matrix.md    per-step agent / CLI / approval map
  references/disclosure-and-compliance.md
proposal/care-circle-proposal.md  the ten proposal answers (455 words; 487 as the PDF renders them)
proposal/care-circle-proposal.pdf the submitted PDF (<= 1 MB)
submission/care-circle-skill.zip  the submitted ZIP (<= 10 MB, 3 files)
submission/devpost-upload.md      the one-screen upload guide: files, track, answers
research/public-submissions.md    the public competitor landscape (70 entries)
research/public-submission-slugs.md  every public Devpost slug found
research/raw-devpost-slugs.txt    the raw scrape behind the slug list
architecture/architecture.md      workflow, state model, failure modes, demo plan
council/                          concept-selection record and judge verdicts
research/                         candidate concepts and competitor landscape
presentation/nov-12-briefing.md    board briefing
video/round-2-script.md           Round 2 demo shot list and narration
round2/demo-assets/               synthetic care folder, expected outputs, 40-check oracle
tools/make_submission.py          renders the proposal PDF and the Skill ZIP
tools/make_demo_assets.py         renders the synthetic Round 2 demo asset set
```

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

## The competitor landscape has changed

The council chose care-circle on a landscape of 11 public entries. There are now
**70 public Devpost software pages**, and medical/care is the densest domain in
them: at least 14, including `Doctor Visit Brief`, `Ubat & Rekod` and
`Family Medicine Register`, which produce substantially the same artifact.

`research/public-submissions.md` is the full record. The consequence: **the
differentiation is no longer cross-modal orchestration — it is the
reconciliation between the family's own documents.** care-circle reads each
medication from its label and from the clinic letter, and reads the current
letter against the earlier one, reports every disagreement with both source
paths, and refuses to resolve it. No public entry in this space claims that
comparison.

The proposal and the Skill description were rewritten on 2026-11-08 to lead with
that step rather than with modality. A second council on 2026-11-08 (five
perspectives, `council/verdict-addendum-2026-11-08.md`) upheld the concept and
sharpened the mechanism: the report-versus-report comparison now uses the
catalog's `ug-document reconcile` action, so half the reconciliation is
vision-independent and survives on camera even if label reading fails.

## Round 2 (finalists)

Invited Nov 21; one day of remote NAS access Nov 22–28; final package and a
three-minute YouTube video due Nov 30.

- `round2/demo-assets/margaret-care-2026-11-08/` — a complete **synthetic** care
  folder (three readable labels, current letter, earlier report, voice memo,
  one unreadable photo). Fictional patient and pharmacy; safe to show on camera.
- `round2/demo-assets/expected/` — the required content of the brief and the
  sibling update, plus a 40-check acceptance list to run on the NAS.
- `video/round-2-script.md` — shot list, narration and failure fallbacks.

```bash
python3 tools/make_demo_assets.py   # regenerate the asset set (needs ffmpeg)
```

## Entrant

Philip Jon Ji Ciuca (individual entry). The Skill and its core workflow were
developed during the hackathon; no previously developed Skill or submission
material is reused.
