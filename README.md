# care-circle — UGREEN Hackathon 2026 on AI NAS

Round 1 submission for the UGREEN Hackathon 2026 on AI NAS (Devpost).
**Track:** Automate Your Workflow.

care-circle turns one folder of medication photos, clinic letters and voice
memos into a dated, source-cited doctor-visit brief and a sibling update,
computed entirely on the NAS. It is pure Markdown orchestration over UGOS
expert agents — no scripts, no external services, no data leaves the device.

## Repository layout

```
skill/care-circle/                 the Uliya Skill package
  SKILL.md                         entry point (required)
  references/workflow-matrix.md    per-step agent / CLI / approval map
  references/disclosure-and-compliance.md
proposal/care-circle-proposal.md  the ten proposal answers (458 words; 490 as the PDF renders them)
proposal/care-circle-proposal.pdf the submitted PDF (<= 1 MB)
submission/care-circle-skill.zip  the submitted ZIP (<= 10 MB, 3 files)
submission/devpost-upload.md      the one-screen upload guide: files, track, answers
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

## Check the Skill

Requires Node and the UGREEN Uliya skill kit v0.7.3.

```bash
node <uliya-skill-kit>/scripts/check-skill.mjs skill/care-circle
# -> status: static-pass, errors 0, warnings 0 (catalog v2.0.0)
```

## Round 1 status

- Official static checker: **static-pass**, 0 errors, 0 warnings, 0 info.
- Proposal: 458 English words in the ten answers; 490 including the section
  headings, so it stays under the 500-word limit on the strictest reading.
- Package: 3 files, 6,198 bytes compressed, 14,534 bytes uncompressed.
- Not yet validated: on-device behaviour of `ug-photo vision-ocr`/`vision-vlm`,
  `ug-document extract` (schema `medical-report`), `ug-knowledge
  audio-transcription`, tag creation and write approval. These are Round 2 items.

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
