# care-circle — board briefing for Philip (Nov 12)

**One line:** care-circle turns a folder of medication photos, clinic letters and
voice memos into a dated, source-cited doctor-visit brief, computed entirely on the
NAS. It is built, checked, packaged and committed.

## The decision

A four-perspective council chose care-circle from ten candidates. It won User Value
(9/10), AI NAS Fit (9/10) and the demand critique (#1). The Innovation judge ranked it
7/10 and preferred incident-dossier (9/10) — rejected because a fresh iDX6011 Pro has
no surveillance history, so that skill cannot demonstrate its central step in Round 2.

**Why care-circle wins:** it is the only candidate that (a) passes the official Uliya
static checker, (b) runs on data a finalist can carry to a fresh NAS, and (c) produces
a source-cited artifact a judge can verify in five seconds.

## What is built

| Deliverable | State |
|---|---|
| `skill/care-circle/SKILL.md` + 2 references | official checker **static-pass**, 0 errors / 0 warnings, catalog v2.0.0 |
| `proposal/care-circle-proposal.pdf` | 7,727 bytes, 458 words in the answers, 490 including headings (limit 500) |
| `submission/care-circle-skill.zip` | 3 files, 6,198 bytes (limits 10 MB / 100 files / 1 MB each) |
| `architecture/architecture.md` | 12-step workflow, approval model, failure modes, demo plan |
| `council/verdict.md` | the decision record and the rejected alternatives |
| GitHub | https://github.com/Philipjj609/ugreen-hackathon-care-circle (private, `main`) |

## The workflow in one breath

File expert enumerates and dedupes the folder → photo expert reads the pill labels
with `vision-ocr`/`vision-vlm` → document expert extracts the clinic letters and
compares each medication against its label → knowledge expert transcribes the voice
memos → orchestrator assembles the brief and a separate five-line sibling update →
**approval gate** → packet folder created, both documents written, sources tagged.

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

## The risks that matter

1. **On-device vision fails on a curved label.** Mitigation: the unreadable list is a
   designed outcome, not an error; the demo still shows the artifact and the conflict
   path through documents.
2. **"It is just a summary."** Mitigation: the output is a saved, tagged file set with
   source paths, not prose in a chat window.
3. **Medical liability perception.** Mitigation: never diagnoses, never advises dosage,
   always prints the clinician-confirmation line.
4. **Tag bootstrap fails.** Mitigation: fallback reports tags unavailable; no file is
   tagged by guess.

## What I need from you

1. **Track:** Automate Your Workflow — confirm or prefer Open Innovation.
2. **Team:** individual entry under your name, or up to three? Who else?
3. **Sponsors/partners:** any to disclose? The disclosure file currently lists none.
4. **GitHub:** private repo committed as Philipjj609 — correct? Public before Nov 15?
5. **Emphasis:** anything to add or remove from the proposal or the Skill?

## What happens next

- **Nov 15** — Round 1 deadline. You submit the PDF + ZIP on Devpost (your account).
- **Nov 21** — finalists invited. If shortlisted, Round 2 is one day of remote NAS
  access (Nov 22–28) and a 3-minute YouTube video due Nov 30.
- **Round 2 prep** — shot list and narration are drafted in `video/round-2-script.md`;
  finalist data prep (which labels to photograph, which conflict to engineer, which
  previous report to bring) is specified in `architecture/architecture.md` §11.
