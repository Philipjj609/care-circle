# UGREEN Hackathon 2026 — public submission landscape (Round 1)

**Compiled:** 2026-11-08, by the CEO from public Devpost software pages and public
GitHub repos. Every entry below is a project a member of the public chose to
publish; the list is evidence about the field, not about what UGREEN has judged.

**Method.** Search engines were queried for public `devpost.com/software/*` pages
and public GitHub repositories naming the hackathon. **70 unique public Devpost
software pages** were found; the health/medication subset was then read in full.
Searches are lossy and the official Devpost project gallery is unpublished until
judging, so this is a **lower bound on the field**, not the full entry list.

## The single most important finding

**The medical/care/medication space is not whitespace — it is one of the most
crowded domains in the public field.** At least **14 public submissions** are
health, medicine or care products, and several do substantially what care-circle
does.

This is a material change to the record. The original council decision
(`council/verdict.md`) was made on a landscape captured early: "11 public entries;
cross-modal orchestration is the open moat". That landscape has grown roughly 6x,
and the moat has been entered.

| Public entry | What it does | Overlap with care-circle |
|---|---|---|
| **Doctor Visit Brief** | Lab + medical reports + prescriptions → one-page brief for the next visit, saved beside the records | **Near-direct.** Same artifact, same modality, same privacy claim |
| **Ubat & Rekod** | Prescription/clinic-slip photos → per-person medication register, duplicate alerts, trilingual visit brief | **Near-direct**, plus translation and a standing register |
| **Family Medicine Register** | Prescriptions, receipts, box photos → per-person register with expiry, source traceability, "unreadable" never guessed | **Near-direct**, register framing |
| **Family Medicine Cabinet** | Medicine-box photos → expiry sort + pharmacy take-back list | Same vision step, expiry angle |
| **Medical Bill Checker** | Bills vs insurance EOBs → cited discrepancy report | Same health-privacy framing, billing |
| Alice, Take Your Meds | Medication adherence companion | Same domain, adherence angle |
| MedBud / MedSafe / MedSNAP / MedTap / MediLens / MedScribe / NANI / dōs / Medicine Tracker / Guardian | Medication management, reminders, identification, dispensing | Same domain, different mechanics |
| Home AI First Aid Kit | First-aid guidance | Same domain, advice (riskier) |

## What is now stale in the record

1. *"Cross-modal orchestration is the open moat."* — `Ubat & Rekod` and
   `Doctor Visit Brief` are both cross-modal (photos + documents + save-back).
   **Cross-modal is now table stakes in the care niche.**
2. *"Surveillance and media/music are untouched."* — Surveillance is **not**
   untouched: `Alibi Docket`, `NAS Incident Triage`, `Project ZERO — Evidence
   Guardian`, `Claim Evidence Pack`, `Home Incident Claim Pack`, `Receiving
   Evidence Reconciler` and `nas-evidence-brief` all occupy it. Local music/video
   media remains thin.
3. *"11 public entries; document-claim verification is crowded."* — the real
   figure is 70 public software pages, and medical is the densest domain.

## What still separates care-circle

The separation is now narrower than the record claims, and must be stated that
way. Four things, in order of how checkable they are:

1. **The label-versus-report reconciliation.** Every public care entry reads
   sources and lists them. **None of the public descriptions claims a
   per-medication agreement/conflict comparison against the clinic letter.** This
   is the one step a judge can watch happen.
2. **Deliberate non-resolution of conflict.** The Skill reports a disagreement
   and refuses to resolve it. Every public entry in this space either resolves
   silently or does not compare at all.
3. **The change-since-the-previous-visit comparison** across two reports.
4. **The sibling update** — a separate five-line, family-facing artifact rather
   than a section of the clinician brief.

**The bet, restated honestly:** care-circle does not win by being cross-modal. It
wins by being the only entry that shows a *disagreement between two of the user's
own documents* and refuses to paper over it.

## Density map of the 70 public entries

| Domain | Count | Examples |
|---|---|---|
| Medicine / health / care | ~14 | Doctor Visit Brief, Ubat & Rekod, Family Medicine Register, Family Medicine Cabinet, Medical Bill Checker, MedBud, MedSafe, MedSNAP, MedTap, MediLens, MedScribe, NANI, dōs, Medicine Tracker |
| Evidence / incidents / insurance / claims | ~9 | Alibi Docket, NAS Incident Triage, Project ZERO, Claim Evidence Pack, Home Incident Claim Pack, Receiving Evidence Reconciler, Deposit Shield, nas-evidence-brief, Asset License Shortlist |
| Documents / contracts / finance / tax | ~8 | Supplier Three-Way Match, Month-End Close Pack, Client Handoff Check, Creator Handoff Preflight, BriefLens, Final Version Finder, Paper Trail, Warranty Receipt Tracker |
| Photos / albums / media / consent | ~10 | Portrait Consent Guardian, Publish-Safe Photo Review, Shared Photo Collector, Photo Event Folders, Shoot Triage, Script to Selects, Memory Lane, Missing Moments, Remembrance Card |
| Home / household / family organisation | ~8 | Homemaker, HomeCompass, Family Recipe Box, NASweep, OctoFile, Clean Set, EverGreen, RelayReady |
| General knowledge / memory / notes | ~6 | Memex for Life, SameName, Echoes, Ember, Nomi, nudge |
| Other / unclear | ~15 | Elsa, Guardian, MentalDrive, Private Family AI Home Cloud, NAS Work Lease, and others |

## Competition density, from a public competitor's own numbers

`github.com/kevin9327/UGREEN_AINAS2026` documents **324 registrations** and
estimates **fewer than 25 expected submissions**. The Devpost API reports 1,714
registrations for the hackathon, but registrations are not submissions. If the
submission estimate holds, **up to 30 finalists from under 25 entries would mean
every eligible entrant advances** — which cannot be right, but the direction is:
this is a low-density competition, and the binding constraint is not beating 25
rivals, it is clearing the eligibility screen and being legible to a judge in the
first page.

That reframes the risk. The threat is not that a better care brief exists. It is
that a judge scanning 25 PDFs finds care-circle's indistinguishable from
`Doctor Visit Brief` at a glance.

## The scoring consequence

The four criteria are equally weighted: User Value, Innovation & Differentiation,
Technical Quality, AI NAS Fit & Validation. Two are scored largely from the PDF
and the ZIP. **Innovation & Differentiation is now the criterion care-circle is
most at risk on**, because a judge who searches the public field will find
near-neighbours, and the proposal described care-circle as "cross-modal" without
naming the reconciliation.

**Fix applied 2026-11-08 (no rebuild):** proposal item 5, item 7, item 9, item 10
and the Skill description now lead with the comparison, not the modality.
Modality is the plumbing; refusing to resolve a conflict between two of the user's
own documents is the product.

## Sources

Public Devpost software pages and public GitHub repositories, retrieved
2026-11-08. Full slug list: `research/public-submission-slugs.md`.

