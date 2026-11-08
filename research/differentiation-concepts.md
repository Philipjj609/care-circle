# Differentiation-led concept set (UGREEN Hackathon 2026)

Whitespace left by the public field: surveillance/security, local music/video media, and cross-domain privacy are untouched; document-claim verification is crowded (omni-claim-guardian, evidence-ledger-nas) and voice-to-story is occupied (family-archive-weaver). All four concepts below exploit catalog capabilities no public entry uses.

---

## 1. `incident-dossier`

- **Track:** Automate Your Workflow
- **What it does:** Turns a physical incident (missed delivery, damage, dispute) into a user-confirmed, hash-chained evidence dossier that correlates local surveillance events and identities with the matching local order/invoice.
- **Target user + problem:** Homeowner or small-shop owner who has a camera event and a paper trail but no way to assemble a third-party-ready evidence packet without uploading footage to a cloud service.
- **Core user flow:**
  1. User states the incident and the order/invoice; the skill confirms the time window and document location (waiting_user if ambiguous).
  2. Delegate to `file-agent` → `ug-filesystem find` (path, pattern, type=documents, date range) to locate the order/invoice.
  3. Delegate to `document-agent` → `ug-document extract` (schema=invoice|receipt|purchase_order) to pull vendor, amount, order id, date.
  4. Delegate to `security-monitor-agent` → `ug-surveillance event-timeline` (start-time/end-time, topic=Package|Vehicle|Human, identity-type=stranger) to get candidate event ids.
  5. Delegate to `security-monitor-agent` → `ug-surveillance identity-resolve` (event-id, include-explanation=true) to identify the person/vehicle and the match explanation.
  6. Confirmation gate (waiting_approval): show the event summary, identity explanation, and evidence plan; user approves purpose and TTL.
  7. Delegate to `security-monitor-agent` → `ug-surveillance event-evidence` (event-id, evidence-type=snapshot|clip, purpose=export_request, ttl-sec) to materialize evidence.
  8. Delegate to `file-agent` → `ug-filesystem sha256sum` on the evidence exports and the source document to build the chain of custody.
  9. Delegate to `knowledge-agent` → `ug-knowledge save-text` to write the dossier (incident, order facts, identity explanation, evidence refs, hashes); approval=workflow, user confirms.
  10. States: completed → deliver dossier path + hashes; failed → report the failing step and stop; cancelled → stop; waiting_user → ask; waiting_approval → hold.
- **What is new:** None of the four public entries touches surveillance or correlates physical events with documents; evidence-ledger-nas and omni-claim-guardian are document-only claim graphs. The mechanism is purpose-scoped, TTL-bound evidence export plus a SHA-256 chain of custody, with explicit user consent before export. Versus cloud AI: footage, identity, and documents never leave the NAS; the dossier is assembled locally and exported only for a declared purpose.
- **Genuine NAS dependence:** Local surveillance event store and on-device face/plate identity model; local document extraction; local file hashing; local LLM for the dossier; privacy (no cloud egress).
- **Biggest risk:** `event-evidence` may be approval-gated or blocked, and `event-timeline` needs a precise window; `identity-resolve` may return unknown, leaving the dossier without a subject. Admissibility of a self-generated dossier is untested.

---

## 2. `album-to-soundtrack`

- **Track:** Unleash Your Creativity
- **What it does:** Translates the semantics of a local photo album into a playable soundtrack drawn only from the NAS's own music library, plus a written liner-notes artifact pairing each track with a photo moment.
- **Target user + problem:** A hobbyist with a large local photo archive and a local music library who wants an evolvable, playable "film" of a trip or event without a cloud music account or manual playlist curation.
- **Core user flow:**
  1. User names an album or photo set ("soundtrack my Iceland trip").
  2. Delegate to `photo-agent` → `ug-photo albums` (keyword) or `ug-photo search-picture` (start-time/end-time) to resolve the album.
  3. Delegate to `photo-agent` → `ug-photo vision-vlm` (path, prompt deriving setting/weather/energy/era/palette) on a sample of key photos; optionally `ug-photo vision-ocr` for signs or lyrics.
  4. Orchestrator reasoning (no delegation): derive a local mood brief (setting, energy, era, palette).
  5. Delegate to `media-agent` → `ug-music search` (type=genre|year|keyword, keyword from the brief; type=library to stay local) to find matching local tracks.
  6. Delegate to `media-agent` → `ug-music control` (operation=set-playback-mode sequential, set-volume) to play the soundtrack.
  7. Delegate to `document-agent` → `ug-document writing` (task=draft, style=friendly, query pairing each track with a photo moment) to draft liner notes.
  8. Delegate to `knowledge-agent` → `ug-knowledge save-text` to save the liner notes + playlist; user confirms.
  9. States: completed → deliver playlist + notes; failed → report; cancelled → stop; waiting_user → ask; waiting_approval → hold.
- **What is new:** FolioRoams generates a portfolio from archived client projects (document-centric); no competitor uses vision-vlm or the music library. The mechanism is cross-modal translation (image semantics → local music attributes) that produces a playable artifact, not a document. Versus cloud AI: no cloud music account, no listening-data upload; the "creative director" is your own photo semantics and the output plays on the NAS.
- **Genuine NAS dependence:** Local photo index and on-device VLM; local music library and media server; local document generation; local compute.
- **Biggest risk:** `ug-music search` has no mood/energy/tempo metadata (genre/year/keyword only), so "mood matching" is approximate; vision-vlm output is unstructured and model quality is unknown, so the soundtrack can feel arbitrary.

---

## 3. `known-circle`

- **Track:** Bring Memories to Life
- **What it does:** Builds a consent-curated ledger of the people who move through your home — each identity is named by you from a security face with an inspectable match explanation, then used to answer "when did X last visit?" and to find matching photos.
- **Target user + problem:** A household that wants a private "who's who / when were they here" memory without auto-tagging biometrics or uploading face data to a cloud photo service.
- **Core user flow:**
  1. User asks "who has been coming and going?" or "find photos of Ana".
  2. Delegate to `security-monitor-agent` → `ug-surveillance faces` (identity-type=stranger) to list unknown faces.
  3. Delegate to `security-monitor-agent` → `ug-surveillance face-detail` (face-id) for the face and its sample events.
  4. Confirmation gate (waiting_approval): the user assigns a name/relationship; the skill never auto-names.
  5. Delegate to `security-monitor-agent` → `ug-surveillance event-timeline` (identity-type=known, person-name=<name>) to build the visit history.
  6. Delegate to `security-monitor-agent` → `ug-surveillance identity-resolve` (event-id, include-explanation=true) to attach an explanation to each match.
  7. Delegate to `photo-agent` → `ug-photo search-picture` (figure-name=<name>) to find matching photos.
  8. Delegate to `knowledge-agent` → `ug-knowledge save-text` to write the circle card (identity, visit history, explanations, photo refs); user confirms.
  9. States: completed → deliver circle card; failed → report; cancelled → stop; waiting_user → ask; waiting_approval → hold.
- **What is new:** family-archive-weaver infers people from voice recordings and auto-builds photo-verified albums; this never auto-names anyone — identity is explicitly curated from security faces with inspectable explanations, and the output is a temporal visit/relationship record, not a story or album. Versus cloud AI: face and identity data stay local, match reasoning is inspectable, and naming is under user control.
- **Genuine NAS dependence:** Local face/identity model and surveillance event store; local photo index; local document generation; privacy (biometrics never leave the NAS).
- **Biggest risk:** Face-recognition accuracy/bias and the ethics of naming people; `identity-resolve` explanations may be shallow; users may not want to curate identities, and biometric data is regulated.

---

## 4. `data-self-audit`

- **Track:** Open Innovation
- **What it does:** Produces a verifiable, hash-chained inventory of what the NAS knows about a person across five domains — files/duplicates, photos and faces, surveillance presence, media taste, documents — then lets the user export or erase file-domain items under explicit consent.
- **Target user + problem:** A privacy-conscious owner who cannot see what their NAS has inferred about them (faces, visits, taste, duplicates) and has no local way to audit and prune it.
- **Core user flow:**
  1. User asks "what does my NAS know about me?".
  2. Delegate to `file-agent` → `ug-filemgr scan-dedupe` (scope=all) to inventory duplicates/storage.
  3. Delegate to `photo-agent` → `ug-photo albums` + `ug-photo figure-albums` to inventory photos and people.
  4. Delegate to `security-monitor-agent` → `ug-surveillance faces` (identity-type=all) + `ug-surveillance event-timeline` (identity-type=all) to inventory identities and presence.
  5. Delegate to `media-agent` → `ug-music search` (type=library|recent) + `ug-video search` (type=recent|library) to inventory media taste.
  6. Delegate to `document-agent` → `ug-document metadata` (directory) to inventory documents.
  7. Orchestrator reasoning (no delegation): assemble the audit dossier; delegate to `knowledge-agent` → `ug-knowledge save-text` to write it; user reviews.
  8. User selects items to erase/export; confirmation gate (waiting_approval).
  9. Delegate to `file-agent` → `file-workflow batch-del` (paths) or `ug-filemgr tag-add-file` (path, tag-id) to quarantine/erase file-domain items; photo/surveillance items are exported and flagged for manual removal (no delete capability in those domains).
  10. States: completed → deliver audit + action log; failed → report; cancelled → stop; waiting_user → ask; waiting_approval → hold.
- **What is new:** omni-claim-guardian and evidence-ledger-nas verify claims inside documents; this audits the NAS's own cross-domain personal data footprint and exercises consent-gated erasure. No competitor addresses data sovereignty. Versus cloud AI: cloud assistants do not provide a verifiable, hash-chained inventory of what they know about you across identity, presence, photos, and media; this is local, inspectable, and user-controlled.
- **Genuine NAS dependence:** Local face/identity and surveillance data; local photo/media libraries; local document metadata; local dedupe and hashing; local compute.
- **Biggest risk:** Erasure is file-domain only (no photo/surveillance delete capability), so the "prune everything" promise is partial; batch deletion is irreversible and must be scoped carefully; "personal data" scope is fuzzy and the audit may surface sensitive material.
