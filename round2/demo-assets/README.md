# care-circle — Round 2 demo asset set

A complete, self-contained care folder so the Round 2 demo can be rehearsed and
recorded without a real patient, and so the Skill has a fixed test oracle.

**Everything here is fictional.** Riverside Pharmacy, Dr A. Rahman, Margaret
Ellison and prescription 8841203 do not exist. The labels, letters and voice
memo were generated for this demo by `tools/make_demo_assets.py`. It is safe to
show on camera and safe to upload to the assigned NAS. Do not substitute a real
patient's data.

## Contents

```
margaret-care-2026-11-08/        the folder to upload and name in the Skill
  01-label-amoxicillin.jpg       readable label, 500 mg capsules
  02-label-atorvastatin.jpg      readable label, 20 mg tablets
  03-label-metformin.jpg         readable label, 850 mg tablets
  04-clinic-letter-2026-11-08.pdf  current clinic letter
  05-voice-memo-2026-11-06.wav   voice memo with two questions
  06-label-unreadable.jpg        deliberately unreadable photo
  07-previous-report-2026-05-12.pdf  the baseline report
alternates/
  voice-memo.m4a                 the same memo in AAC, if WAV is rejected
expected/
  brief-required.md              what the care brief must contain
  sibling-update-required.md     what the sibling update must contain
  checks.md                      pass/fail tests to run on the NAS
```

## The story

Margaret Ellison, 74, has type 2 diabetes and hypertension. She attends an
outpatient review on 8 November 2026. Her daughter has photographed three pill
labels, saved the clinic letter, recorded a short voice memo on 6 November, and
found a fourth photo that is too blurred to read. The previous clinic letter from
12 May 2026 is in the same folder so the "changes since the previous visit"
comparison has a real baseline.

## What the set is engineered to demonstrate

| Demonstration | Where it comes from |
|---|---|
| Label and report **agree** | `02-label-atorvastatin.jpg` (20 mg) against the letter's "Atorvastatin 20 mg at night" |
| Label and report **conflict** | `03-label-metformin.jpg` says 850 mg; the letter says 500 mg twice daily |
| Label with **no report entry** | `01-label-amoxicillin.jpg` — the letter lists no antibiotic |
| **Unreadable** file handled honestly | `06-label-unreadable.jpg` — a fourth medication, not a copy of a label in the folder, so dedupe cannot collapse the pair |
| **Change since the previous visit** | Atorvastatin started; HbA1c 7.1 → 6.9; LDL measured for the first time; eGFR 78 → 80 |
| **Questions for the doctor** | the two questions in the voice memo |
| **Results and findings** | HbA1c, blood pressure, LDL, eGFR; dizziness and ankle swelling |

The conflict is deliberate. It is the best moment in the demo: the Skill must
flag it with both source paths and must **not** resolve it.

## Using it on the NAS

1. Upload `margaret-care-2026-11-08` to the assigned NAS.
2. Invoke care-circle. Name the folder, the parent (Margaret) and the appointment
   date (8 November 2026). That is the only input.
3. Walk the twelve steps. Approve the brief at the gate.
4. Compare the result against `expected/checks.md`.

## If the on-device vision cannot read a rendered label

Rendered labels are cleaner than real phone photos, so this should not happen —
but if it does, the demo still works: the letter carries the same medications,
so the conflict, the change-since-visit and the artifact are all still visible.
Say "it could not read this one" and move on. The unreadable list is a designed
outcome, not a failure.

## Regenerating

```bash
python3 tools/make_demo_assets.py
```

Requires `ffmpeg` on PATH and the Windows fonts `arial.ttf` and `arialbd.ttf`.
The script writes into this directory and prints the size of every file.
