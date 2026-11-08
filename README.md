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
proposal/care-circle-proposal.md  the ten proposal answers (485 words)
proposal/care-circle-proposal.pdf the submitted PDF (<= 1 MB)
submission/care-circle-skill.zip  the submitted ZIP (<= 10 MB, 3 files)
architecture/architecture.md      workflow, state model, failure modes, demo plan
council/                          concept-selection record and judge verdicts
research/                         candidate concepts and competitor landscape
presentation/nov-12-briefing.md    board briefing
video/round-2-script.md           Round 2 demo shot list and narration
tools/make_submission.py          renders the proposal PDF and the Skill ZIP
```

## Build the deliverables

```bash
python3 tools/make_submission.py
# -> dist/care-circle-proposal.pdf and dist/care-circle-pretest-skill.zip
```

## Check the Skill

Requires Node and the UGREEN Uliya skill kit v0.7.3.

```bash
node <uliya-skill-kit>/scripts/check-skill.mjs skill/care-circle
# -> status: static-pass, errors 0, warnings 0 (catalog v2.0.0)
```

## Round 1 status

- Official static checker: **static-pass**, 0 errors, 0 warnings, 0 info.
- Proposal: 485 English words across the ten items (limit 500).
- Package: 3 files, 5,745 bytes compressed, 13,366 bytes uncompressed.
- Not yet validated: on-device behaviour of `ug-photo vision-ocr`/`vision-vlm`,
  `ug-document extract` (schema `medical-report`), `ug-knowledge
  audio-transcription`, tag creation and write approval. These are Round 2 items.

## Entrant

Philip Jon Ji Ciuca (individual entry). The Skill and its core workflow were
developed during the hackathon; no previously developed Skill or submission
material is reused.
