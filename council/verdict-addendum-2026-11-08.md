# Council addendum — the crowded-field re-test

**Date:** 2026-11-08. **Decided by:** CEO, on council evidence.
**Scope:** a re-test of the concept decision in `council/verdict.md`, triggered by
new evidence, not a fresh concept selection.

## Trigger

`research/public-submissions.md` (same day) found **70 public Devpost software
pages** where the original council saw 11. Medical/care is the densest domain in
them — at least **14 entries**, including three that produce substantially the
same artifact: `Doctor Visit Brief`, `Ubat & Rekod`, `Family Medicine Register`.
The original verdict's load-bearing claim — "cross-modal orchestration is the
open moat" — is false: at least two near-neighbours are cross-modal.

## Question put to the council

1. Keep care-circle and sharpen the differentiation around the
   label-versus-letter reconciliation, pivot to a thinner domain, or reposition
   the artifacts and messaging?
2. Should the Devpost track stay **Automate Your Workflow** or move to
   **Open Innovation**?

Five perspectives were dispatched in parallel against the same evidence: User
Value, Innovation & Differentiation, Technical Quality & Feasibility, AI NAS Fit
& Round 2 Demo, and a red team instructed to break the plan. Each returned a
verdict plus the strongest objection to its own position.

## Verdicts

| Perspective | Verdict | Track | Conf. | Core reasoning |
|---|---|---|---|---|
| User Value | keep_sharpen | automate | 7 | The reconciliation is the one thing a caregiver cannot check themselves; the crowded field is a legibility problem, not a product problem. |
| Innovation & Differentiation | **reposition** | **open_innovation** | 7 | The comparison is a prompt, not a mechanism — a generic multimodal LLM obeys it. The governance pipeline is the real moat, so lead with the escalation contract. |
| Technical Quality | keep_sharpen | automate | 7 | `ug-document qa`'s only document input is `file`; the step-3 label rows have no parameter, so "not a summary" was a prompt aspiration. Also found the proposal/README inconsistency. |
| AI NAS Fit & Demo | keep_sharpen | automate | 7 | `ug-document extract` ships a `mixed_reconciliation` schema and `ug-document reconcile` exists; the conflict is vision-dependent and vanishes if OCR fails. |
| Red team | **reposition** | automate | 6 | Round 1 scores are discarded — winners are decided by Round 2 only. Item 1 still led with "doctor-visit brief" while the nearest neighbour is literally named `Doctor Visit Brief`. |

**Tally:** keep the concept 5/5. Keep-sharpen 3, reposition 2. Track: Automate 4,
Open Innovation 1.

## Synthesis — what was decided

**The concept stays. The first-page framing changes. The mechanism is made
catalog-native.** The two "reposition" votes were not a vote to abandon
care-circle; both explicitly said a pivot is not executable in seven days and
that every alternative is worse. They won on the *framing*, and that fix is
absorbed.

The reconciliation was restated as one product with two halves, which resolves
the keep-sharpen/reposition split:

1. **Label versus letter** — each medication read from its pill bottle and from
   the clinic letter. Depends on on-device vision.
2. **Letter versus earlier letter** — each medication read from the current
   report and from the earlier one. **Document-only.**

Both report the disagreement with both source paths and neither resolves it.
Framing the product as "reports every disagreement between the family's own
documents" is simultaneously the comparison (keep_sharpen) and the escalation
contract (reposition) — they were never different ideas.

## Rejected, and why

- **Pivot to a thinner domain.** Not executable before Nov 15 without forfeiting
  the 9/10 User Value and 9/10 AI NAS Fit scores, and every alternative field is
  also crowded (evidence/claims ~9, photos ~10, household ~8). The original
  council's rejections of incident-dossier, known-circle, data-self-audit and
  album-to-soundtrack still stand.
- **Move to Open Innovation.** Lost 4-1. The Automate mission text — "organize
  content, extract information, generate summaries, and automate repetitive
  tasks" — describes care-circle literally; Open Innovation is the catch-all
  bucket where the Innovation criterion, care-circle's weakest at 7/10, is the
  explicit mission. The dissent is recorded and the board may override.
- **"Refuses to resolve" as the headline.** A restraint is not a new function,
  and the Innovation criterion asks for one. The headline is the *report* of the
  disagreement; the non-resolution is a property of it, not the product.

## Defects found and fixed

1. **First-page collision.** Proposal item 1 led with "doctor-visit brief"
   while a near-neighbour is named `Doctor Visit Brief`. Item 1 and the Devpost
   tagline now lead with the disagreement between the family's own documents.
2. **Proposal/README inconsistency.** Item 8 called the comparisons
   "implemented" while the README's not-yet-validated list omitted them. Item 8
   now lists both comparisons as pending NAS validation, and the README list
   includes them.
3. **Mechanism overclaimed.** Step 5 implied `ug-document qa` could take the
   step-3 label rows as input; `qa`'s only document parameter is `file`. Step 5
   now carries the label rows in the query, and the report-versus-report half
   uses the catalog's `ug-document reconcile` action over the report paths.
4. **Demo overclaim.** The asset README claimed the conflict survives a vision
   failure. It does not — without a label reading there is nothing to compare.
   The README now states that the document-only half survives and the
   label-versus-letter half does not.

## Verification record

- `python3 tools/make_submission.py` → 455 words answers-only, 487 as the PDF
  renders them (limit 500); PDF 7,751 bytes, 2 pages; ZIP 6,371 bytes, 3 files.
- `node vendor/uliya-skill-kit/scripts/check-skill.mjs skill/care-circle` →
  `static-pass`, errors 0, warnings 0, info 0 (catalog v2.0.0).
- `ug-document reconcile` confirmed present in catalog v2.0.0 with a repeatable
  `file` parameter and a cross-document example.
