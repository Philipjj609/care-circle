# care-circle — board briefing for Philip (Nov 12)

**One line:** care-circle reads a family's care folder and reports every
disagreement between their own documents — a pill bottle against a clinic
letter, or one clinic letter against an earlier one — naming both sources and
leaving the disagreement for the clinician. It is built, checked, packaged and
committed.

## The decision

A four-perspective council chose care-circle from ten candidates. It won User Value
(9/10), AI NAS Fit (9/10) and the demand critique (#1). The Innovation judge ranked it
7/10 and preferred incident-dossier (9/10) — rejected because a fresh iDX6011 Pro has
no surveillance history, so that skill cannot demonstrate its central step in Round 2.

**Why care-circle wins:** it is the only candidate that (a) passes the official Uliya
static checker, (b) runs on data a finalist can carry to a fresh NAS, and (c) produces
a source-cited artifact a judge can verify in five seconds.

## What changed on Nov 8, and why it matters

The council chose care-circle on a landscape of **11 public entries**. A fresh sweep
the same day found **70 public Devpost software pages**, and medical/care is the
densest domain in them — at least **14**, including `Doctor Visit Brief`,
`Ubat & Rekod` and `Family Medicine Register`, which produce substantially the same
artifact. The original verdict's claim that "cross-modal orchestration is the open
moat" is **false**: at least two near-neighbours are cross-modal.

A second council was run the same day — five perspectives, including a red team told
to break the plan. Full record: `council/verdict-addendum-2026-11-08.md`.

**The verdict: keep the concept 5/5, keep-sharpen 3 / reposition 2, track Automate 4
/ Open Innovation 1.** No pivot is executable in seven days without forfeiting the
9/10 User Value and 9/10 AI NAS Fit scores.

**The bet, restated:** care-circle does not win by being cross-modal. It wins by being
the only entry that shows a *disagreement between two of the user's own documents*
and refuses to paper over it. The reconciliation has two halves:

| Half | Sources | Needs vision? |
|---|---|---|
| Label versus letter | pill bottle ↔ clinic letter | yes |
| Letter versus earlier letter | current report ↔ earlier report | **no** |

The second half is document-only, so it survives on camera even if the on-device
vision fails — which was the single biggest demo risk.

## What is built

| Deliverable | State |
|---|---|
| `skill/care-circle/SKILL.md` + 2 references | official checker **static-pass**, 0 errors / 0 warnings, catalog v2.0.0 |
| `proposal/care-circle-proposal.pdf` | 7,751 bytes, 455 words in the answers, 487 including headings (limit 500) |
| `submission/care-circle-skill.zip` | 3 files, 6,371 bytes (limits 10 MB / 100 files / 1 MB each) |
| `architecture/architecture.md` | 12-step workflow, approval model, failure modes, demo plan |
| `council/verdict.md` + `council/verdict-addendum-2026-11-08.md` | the decision record and the crowded-field re-test |
| `research/public-submissions.md` | the 70-entry public landscape |
| GitHub | https://github.com/Philipjj609/ugreen-hackathon-care-circle (private, `main`) |

## The workflow in one breath

File expert enumerates and dedupes the folder → photo expert reads the pill labels
with `vision-ocr`/`vision-vlm` → document expert extracts the clinic letters, compares
each medication against its label, and reconciles the current letter against the
earlier one → knowledge expert transcribes the voice memos → orchestrator assembles
the brief and a separate five-line sibling update → **approval gate** → packet folder
created, both documents written, sources tagged.

Every claim carries its source path. Every unreadable file is listed. The brief never
diagnoses and never advises dosage; it ends with "a clinician must confirm every
entry".

## What we found and fixed

The AI NAS Fit judge caught a real defect: step 11 used `tag-list` → `tag-add-file`,
which fails on a fresh NAS because no tags exist and the Skill never created them.
Fixed to `tag-get-by-name` → `tag-add` → `tag-add-file`.

A second catalog re-audit then checked every parameter the Skill relies on, not just
the action names the official checker validates. Three more defects, all fixed:

1. `ug-photo vision-ocr` takes a **single** path, so step 3 now runs one call per
   image instead of implying a batch call.
2. `ug-filemgr tag-add` requires `tag-id`, not a name, so step 11 now sets `tag-id`
   to the tag name explicitly.
3. The sibling update was listed both as a section of the brief and as its own output
   path. It is now a separate document with its own `save-text` call.

These are exactly the failures that would have been visible on camera in Round 2.

**During the crowded-field re-test.** Four more:

1. **First-page collision.** Proposal item 1 led with "doctor-visit brief" while a
   near-neighbour is literally named `Doctor Visit Brief`. Item 1 and the Devpost
   tagline now lead with the disagreement.
2. **Proposal/README inconsistency.** Item 8 called the comparisons "implemented"
   while the README's pending-validation list omitted them. Both now list them as
   pending NAS validation.
3. **Mechanism overclaimed.** Step 5 implied `ug-document qa` could take the label
   rows as input; its only document parameter is `file`. The label rows now travel
   in the query, and the report-versus-report half uses the catalog's
   `ug-document reconcile` action.
4. **Demo overclaim.** The asset README claimed the conflict survives a vision
   failure. It does not. The README now says the document-only half survives and the
   label half does not.

## The risks that matter

1. **A judge confuses it with `Doctor Visit Brief`.** Mitigation: item 1, the tagline
   and the Skill description now all lead with the disagreement, not the artifact
   shape.
2. **On-device vision fails on a curved label.** Mitigation: the change-since-visit
   half is document-only and still lands; the unreadable list is a designed outcome,
   not an error.
3. **"It is just a summary."** Mitigation: the output is a saved, tagged file set with
   source paths, not prose in a chat window — and the comparison is a separate catalog
   call, not a summary.
4. **"Refuses to resolve" reads as a missing answer.** Mitigation: it is framed as a
   clinician-decides safety gate, and the brief ends with the clinician-confirmation
   line.
5. **Tag bootstrap fails.** Mitigation: fallback reports tags unavailable; no file is
   tagged by guess.
6. **The reconciliation has never run on a real NAS.** Mitigation: it is explicitly
   listed as pending validation, with a 40-check oracle and a document-only fallback
   beat in the video.

## What I need from you

1. **Track:** Automate Your Workflow — the council split 4-1 to keep it. Confirm, or
   prefer Open Innovation.
2. **Team:** individual entry under your name, or up to three? Who else?
3. **Sponsors/partners:** any to disclose? The disclosure file lists none.
4. **GitHub:** private repo committed as Philipjj609 — correct? Public before Nov 15?
5. **Emphasis:** anything to add or remove from the proposal or the Skill?

## What happens next

- **Nov 15** — Round 1 deadline. You submit the PDF + ZIP on Devpost (your account).
  `submission/devpost-upload.md` is the one-screen guide.
- **Nov 21** — finalists invited. If shortlisted, Round 2 is one day of remote NAS
  access (Nov 22–28) and a 3-minute YouTube video due Nov 30.
- **Round 2 prep** — shot list and narration are drafted in `video/round-2-script.md`;
  finalist data prep (which labels to photograph, which conflict to engineer, which
  previous report to bring) is specified in `architecture/architecture.md` §11.
- **Note:** Round 1 scores do not carry over — winners are decided by Round 2 only.
  The Round 1 reframe buys a finalist slot; the prize is won on the NAS.
