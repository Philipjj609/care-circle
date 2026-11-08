# care-circle — Round 2 demo video script (target: under 3 minutes)

**Format:** YouTube, public, English narration or complete English subtitles.
**Constraint:** judges are not required to watch beyond three minutes.
**Device:** one assigned iDX6011 Pro (64GB), one testing day, fresh state.

## The principle

Show the artifact early. A judge should see a real folder go in and a real, checkable
document come out within the first 30 seconds. Everything after that is confirmation.

## Pre-recording prep (do this before the testing day)

- Curate 4–6 files in one folder:
  - 2–3 straight-on, well-lit photos of **printed** pill labels (no handwriting).
  - 1 clean clinic letter PDF.
  - 1 short voice memo in a supported format.
  - 1 deliberately blurry photo (this is the honest-unreadable demo).
- Bring a **previous-visit report** so "changes since last visit" has a baseline.
- Engineer **one deliberate conflict**: a label whose dose differs from the letter.
  The conflict row is the best moment in the video; do not leave it to chance.
- Pre-test one label with `ug-photo vision-vlm`. If the local model is weak, lead with
  the document + audio path and keep the photo step short.
- Pre-create the three tags on the assigned NAS in the first 30 seconds, or rely on the
  Skill's `tag-get-by-name` → `tag-add` bootstrap.
- Record a fallback take on a second small folder.

## Shot list

| Time | Picture | Narration (subtitles) |
|---|---|---|
| **0:00** | Cold open: UGOS desktop on the fresh NAS, empty. Finalist uploads the care folder — 3 label photos, 1 letter, 1 memo, 1 blurry photo. | "Fresh NAS, nothing pre-loaded. This is my dad's folder: pill bottles, a clinic letter, and a voice memo. In the next three minutes it becomes a brief I can hand to his doctor." |
| **0:20** | The Skill is invoked. Step 1: folder, parent name, appointment date confirmed. | "I name the folder, my father, and the appointment. That is the only input." |
| **0:30** | File expert enumerates and dedupes; photo expert runs `vision-ocr` and `vision-vlm`. The medication table appears — drug, dose, frequency, source path per row. | "It reads the pill bottles, not just the PDFs — and every row names the file it came from." |
| **1:00** | Document expert extracts the letter; `ug-document qa` compares each medication against its label. A conflict row appears with both source paths. Voice memo is transcribed. | "It caught that the label and the letter disagree on the dose. That is the question for the doctor — and it is flagged, not silently resolved." |
| **1:30** | The brief assembles: medications, recent results, changes since last visit, questions, unreadable list — plus a separate five-line sibling update. | "Current medication, recent results, what changed since last time, and the questions we want to ask." |
| **2:00** | Approval gate pauses. Finalist approves. Packet folder created, brief saved, sources tagged. File tree shows the tagged sources. | "Nothing leaves the NAS. I approve the brief, it is written to a care folder, and every source is tagged in place." |
| **2:30** | Sibling update read aloud (five lines). Unreadable list and confirmation line held on screen. | "My sister gets five lines she can read in a minute. The blurry photo is listed as unreadable — the Skill would rather say nothing than guess." |
| **2:45** | Final shot: the brief's path in the NAS file manager. End card: `care-circle`. | "Every claim is a local file with a source path, and every entry still needs a clinician's confirmation. That is care-circle." |

## Narration notes

- Speak plainly; no hype. The artifact is the story.
- Say the word **unreadable** on camera. Honesty about limits is a judging advantage.
- Say **"nothing leaves the NAS"** once, at 2:00. It is the privacy claim; do not repeat it.
- Do not claim the Skill diagnoses or advises dosage. It organises and surfaces.

## If something fails on the day

- **Vision returns unreadable for a label:** keep the row on screen, say "it could not
  read this one", and move on. The unreadable list is a designed outcome.
- **Transcription is empty:** say so, show the memo marked missing in the brief.
- **Tag creation is blocked:** show the fallback message; the brief and the sources are
  still the deliverable.
- **Any step hangs:** cut to the file tree and the brief; the artifact is the point.

## Submission checklist (Nov 30)

- [ ] Video uploaded to YouTube, set to public, link on the Devpost final-round form.
- [ ] Under three minutes; English narration or complete English subtitles.
- [ ] Final Skill package passes the official checker and runs on the assigned NAS.
- [ ] Project remains available free of charge for judging until Dec 5.
