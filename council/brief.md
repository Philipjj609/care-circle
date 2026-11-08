# Council brief — UGREEN Hackathon 2026: pick ONE Skill concept

Workspace: `C:/Users/phili/Desktop/Projects/ugreen-hackathon`
Read these before answering:
- `scratch/raw/devpost-rules.txt` (official rules; Round 1 = PDF + ZIP, no NAS, no video)
- `research/skill-concepts.md` (candidates A–C, with scores)
- `research/differentiation-concepts.md` (candidates D–G + competitor landscape)
- `scratch/check/concepts2.py` (candidates H–J, full orchestration)
- `scratch/check/household-paper-trail/SKILL.md` (example of a built candidate)
- `vendor/uliya-skill-kit/data/capability-catalog.json` (catalog v2.0.0 — the only legal CLIs)
- `scratch/catalog-summary.md` (readable catalog summary)

## The decision

Pick ONE Skill concept to build and submit. It must (a) survive Round 1 judging on
paper and (b) be demoable in a 3-minute Round 2 video on a fresh iDX6011 Pro with
only the data the finalist brings. Round 2 is one day of remote NAS access.

## Judging criteria — equally weighted, score 1–10 each

1. **User Value** — clear problem, clear workflow, useful feedback, real result.
2. **Innovation & Differentiation** — a substantive new function, interaction or workflow.
3. **Technical Quality** — sound orchestration, correct use of supported CLI
   capabilities and expert agents, permissions and error handling, reliability.
4. **AI NAS Fit & Validation** — meaningful use of NAS capabilities (local data,
   storage, computing, privacy), not merely running on NAS.

## Hard constraints

- The Skill is **pure Markdown orchestration**. No scripts, no direct CLI calls, no
  external services. Only `delegate --target <agent> --instruction '<task>'`.
- Only catalog v2.0.0 CLIs via their registered expert agents
  (file-agent, document-agent, knowledge-agent, photo-agent, media-agent,
  security-monitor-agent).
- Must be newly developed during the hackathon; no reused Skills or materials.
- Third-party components must be disclosed; config examples use placeholders only.
- Pick one track: Automate Your Workflow / Bring Memories to Life /
  Unleash Your Creativity / Open Innovation.

## Candidates

- **A. care-circle** — medication photos + medical reports + parent voice memos →
  doctor-ready one-page brief + weekly sibling update.
- **B. sunday-reset** — weekly scan of school notices, bills, letters, kids' photos,
  voice memos → one-page action brief (sign/pay/decide) + week album.
- **C. tax-packet** — a year of invoices, receipts, contracts, bank PDFs →
  source-cited tax packet with missing receipts, conflicts, filing checklist.
- **D. incident-dossier** — physical incident → consent-gated, hash-chained evidence
  dossier correlating surveillance events + identities with the order/invoice.
- **E. album-to-soundtrack** — photo album semantics → playable soundtrack from the
  NAS's own music library + liner notes pairing tracks to photo moments.
- **F. known-circle** — consent-curated ledger of who comes and goes, named by the
  user from security faces, answerable as visit history + matching photos.
- **G. data-self-audit** — verifiable hash-chained inventory of what the NAS knows
  about a person across files/photos/surveillance/media/documents, with
  consent-gated erasure of file-domain items.
- **H. household-paper-trail** — document folder → cited answers, expiry/renewal
  action list, re-run diff. (built)
- **I. consent-and-release-ledger** — named people in the photo library reconciled
  against release/consent/voice records → publish/review/block grading + tags. (built)
- **J. archive-sync-negotiator** — audio memo transcribed, its claims checked against
  documents and photos → contradiction report + reconciliation album. (built)

## Known competitor landscape (public Devpost gallery)

Document claim-verification is crowded (omni-claim-guardian, evidence-ledger-nas);
voice-to-story is occupied (family-archive-weaver); document dossiers/expiry diffs
exist (Haven, Where It Is); back-office exists (Craft Back Office); portfolio
generation exists (FolioRoams). Surveillance/security, local music/video media and
cross-domain privacy are reportedly untouched.

## Return format (strict)

1. `RANKING` — every candidate A–J with a score 1–10 and a one-line reason.
2. `WINNER` — the single concept you would bet on, and why it beats the runner-up.
3. `LOSS_RISK` — the single strongest reason your winner could still lose.
4. `IMPROVEMENT` — one concrete change that raises your winner's weakest criterion.
5. `TRACK` — which of the four tracks it enters.

Be decisive. No hedging. You are a judge with one vote, not a committee.
