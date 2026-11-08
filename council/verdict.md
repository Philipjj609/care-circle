# Council verdict — UGREEN Hackathon 2026 concept selection

**Decision:** build and submit **care-circle**.
**Track:** Automate Your Workflow.
**Date:** 2026-11-08. **Decided by:** CEO, on council evidence.

## Method

Four independent perspectives were dispatched in parallel against the same brief
(`council/brief.md`): User Value, Innovation & Differentiation, Technical Quality,
and AI NAS Fit. Each read the official rules, the capability catalog v2.0.0, the
candidate set and the built Skills, and returned a ranked verdict. Two perspectives
completed in the first round; the Technical and AI NAS Fit perspectives were retried
and AI NAS Fit completed. Technical Quality was covered by the official static checker
plus the AI NAS Fit judge's catalog verification. A demand-side critique from the
prior run (`council/demand-critic-ranking.md`) was also admitted as evidence.

## Verdicts

| Perspective | Winner | care-circle | Key reasoning |
|---|---|---|---|
| User Value | **care-circle (9/10)** | 9 | Weekly, high-stakes, cross-modal; the brief cites every source and lists what it could not read. Runner-up sunday-reset (8) is "AI-summary shaped". |
| Innovation | incident-dossier (9/10) | 7 | care-circle's core move is multimodal summarisation, which a generic multimodal LLM could imitate; incident-dossier's chain of custody is genuinely new. |
| AI NAS Fit | **care-circle (9/10)** | 9 | Privacy is the product: labels, letters and voice are read, compared and stored on-device. Beats any single-modal alternative for Round 2. |
| Demand critique | **care-circle (#1)** | 1 | Deepest recurrent pain on the list; the strongest "who else loses" story. |

## Synthesis

**care-circle wins, 3 of 4 perspectives.** The Innovation perspective is the
dissenter, and its objection was weighed seriously: care-circle is not a new
*mechanism*. It is a new *composition* — on-device vision over pill labels, medical
report extraction, voice transcription, and a label-versus-report conflict check, all
bound to source files and written back to the NAS — and that composition is exactly
what the AI NAS Fit and User Value judges scored highest.

The Innovation judge's own winner, **incident-dossier, is rejected** for a decisive
practical reason the judge itself named: Round 2 runs on a fresh iDX6011 Pro with only
the data the finalist brings. A fresh NAS has an empty surveillance event store, so the
dossier's central step (`ug-surveillance event-timeline`) returns nothing and the
three-minute demo shows a skill that cannot demonstrate its function. The same
objection applies to known-circle (F). data-self-audit (G) promises erasure it cannot
deliver because the catalog exposes no photo or surveillance delete. album-to-soundtrack
(E) is uncheckable because `ug-music search` carries no mood metadata. The three
document-centric candidates (H, I, J) fail the official static checker outright and
occupy the most crowded space in the public field.

**The bet:** the winner is the skill that shows a real folder of mixed family files
going in and a real, checkable artifact coming out in the first 30 seconds of a fresh
NAS. care-circle is the only candidate that (a) passes the checker, (b) works with data
a finalist can carry, and (c) produces a source-cited artifact a judge can verify.

## Defect found and fixed during council

The AI NAS Fit judge found that step 11 (`ug-filemgr tag-list` → `tag-add-file`) is
guaranteed to fail on a genuinely fresh NAS: `tag-list` returns no tags, and the Skill
never created them. **Fixed:** step 11 now resolves each tag with
`ug-filemgr tag-get-by-name`, creates a missing tag with `ug-filemgr tag-add`, then
applies it with `ug-filemgr tag-add-file`. Re-checked: `static-pass`, 0 errors,
0 warnings.

## Rejected alternatives — one line each

- **sunday-reset (B):** real pain, but the most AI-summary-shaped candidate; deadline
  extraction from photographed notices is its weakest and most consequential step.
- **tax-packet (C):** annual, not recurring; money accuracy is the trust breaker;
  Craft Back Office already owns back office.
- **incident-dossier (D):** strongest novelty, fatal fresh-NAS demo risk.
- **album-to-soundtrack (E):** playful, but arbitrary and uncheckable.
- **known-circle (F):** fresh-NAS face data absent; biometric ethics and regulation.
- **data-self-audit (G):** erasure promise partially undeliverable with catalog v2.0.0.
- **household-paper-trail (H), consent-and-release-ledger (I), archive-sync-negotiator (J):**
  all three fail the official static checker; document-claim verification is the most
  crowded space in the field.

## Verification record

- `node vendor/uliya-skill-kit/scripts/check-skill.mjs skill/care-circle` →
  `static-pass`, errors 0, warnings 0, info 0 (catalog v2.0.0).
- All 13 CLIs used by the Skill verified present in catalog v2.0.0 with the expected
  approval levels (AI NAS Fit judge).
