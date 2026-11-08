#!/usr/bin/env python3
"""Generate the synthetic Round 2 demo asset set for care-circle.

Everything here is FICTIONAL. No real patient, pharmacy, prescriber,
prescription or clinic is depicted. The files exist so a Round 2 finalist can
rehearse and record the demo without needing a real care folder, and so the
Skill's behaviour has a fixed test oracle.

Requires:
  * ffmpeg on PATH          (images, blur, flite voice synthesis)
  * arial.ttf, arialbd.ttf  (Windows fonts, copied into a temp build dir)

The font files are copied to a temp dir and referenced by a RELATIVE path
because an absolute Windows path contains a colon, which ffmpeg's filter
parser treats as an option separator.

Usage:
    python3 tools/make_demo_assets.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "round2", "demo-assets")
CARE = os.path.join(OUT, "margaret-care-2026-11-08")
ALT = os.path.join(OUT, "alternates")
EXPECTED = os.path.join(OUT, "expected")

sys.path.insert(0, os.path.join(ROOT, "tools"))
from make_submission import build_pdf, parse  # noqa: E402

W, H = 1200, 1600
FONT_DIR = r"C:\Windows\Fonts"
FONTS = ["arial.ttf", "arialbd.ttf"]

PHARMACY = "Riverside Pharmacy"
PHARMACY_SUB = "PRESCRIPTION LABEL  -  12 Harbour Road  -  Tel 020 7946 0011"
PATIENT = "Margaret Ellison"
SYNTHETIC = "Synthetic demo label - not a real prescription."


def sh(args, cwd):
    subprocess.run(args, cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_text(build, name, text):
    path = os.path.join(build, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return name


def barcode(x0, y0, h, seed, width=1080):
    """Deterministic pseudo-barcode as a chain of drawbox filters."""
    parts, x, n = [], x0, 0
    while x < x0 + width:
        w = 2 + ((seed * (n + 7) * 2654435761) >> 24) % 9
        if n % 3 != 1:
            parts.append("drawbox=x=%d:y=%d:w=%d:h=%d:c=black:t=fill"
                         % (x, y0, w, h))
        x += w + 2 + ((seed * (n + 13) * 40503) >> 20) % 5
        n += 1
    return parts


def make_label(build, out_path, drug, dose, directions, quantity, rxno, date,
               prescriber, seed):
    lines = [
        ("drawbox=x=0:y=0:w=%d:h=170:c=0x1f4e79:t=fill" % W),
        ("drawtext=fontfile=arialbd.ttf:textfile=f_pharmacy.txt:"
         "fontcolor=white:fontsize=62:x=60:y=38"),
        ("drawtext=fontfile=arial.ttf:textfile=f_sub.txt:"
         "fontcolor=0xcfe0f0:fontsize=30:x=60:y=118"),
        ("drawtext=fontfile=arialbd.ttf:textfile=f_patient.txt:"
         "fontcolor=black:fontsize=44:x=60:y=235"),
        ("drawtext=fontfile=arial.ttf:textfile=f_date.txt:"
         "fontcolor=black:fontsize=40:x=60:y=300"),
        ("drawtext=fontfile=arial.ttf:textfile=f_rx.txt:"
         "fontcolor=black:fontsize=40:x=60:y=365"),
        ("drawtext=fontfile=arialbd.ttf:textfile=f_drug.txt:"
         "fontcolor=black:fontsize=96:x=60:y=500"),
        ("drawtext=fontfile=arial.ttf:textfile=f_dose.txt:"
         "fontcolor=black:fontsize=60:x=60:y=610"),
        ("drawtext=fontfile=arial.ttf:textfile=f_dir.txt:"
         "fontcolor=black:fontsize=46:x=60:y=712"),
        ("drawtext=fontfile=arial.ttf:textfile=f_qty.txt:"
         "fontcolor=black:fontsize=46:x=60:y=788"),
        ("drawtext=fontfile=arial.ttf:textfile=f_presc.txt:"
         "fontcolor=black:fontsize=46:x=60:y=864"),
        ("drawtext=fontfile=arial.ttf:textfile=f_warn.txt:"
         "fontcolor=0x8a1c1c:fontsize=40:x=60:y=944"),
    ] + barcode(60, 1080, 150, seed) + [
        ("drawtext=fontfile=arial.ttf:textfile=f_synth.txt:"
         "fontcolor=0x666666:fontsize=26:x=60:y=1500"),
    ]
    write_text(build, "f_pharmacy.txt", PHARMACY)
    write_text(build, "f_sub.txt", PHARMACY_SUB)
    write_text(build, "f_patient.txt", "Patient:  " + PATIENT)
    write_text(build, "f_date.txt", "Date:  " + date)
    write_text(build, "f_rx.txt", "Prescription:  " + rxno)
    write_text(build, "f_drug.txt", drug)
    write_text(build, "f_dose.txt", dose)
    write_text(build, "f_dir.txt", directions)
    write_text(build, "f_qty.txt", quantity)
    write_text(build, "f_presc.txt", prescriber)
    write_text(build, "f_warn.txt", "Warning: keep out of the reach of children.")
    write_text(build, "f_synth.txt", SYNTHETIC)
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "color=c=0xf7f7f5:s=%dx%d:d=1" % (W, H),
        "-vf", ",".join(lines), "-frames:v", "1", out_path], cwd=build)


def make_blurry(build, src_path, out_path):
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", src_path,
        "-vf", "gblur=sigma=32,noise=alls=20:allf=t",
        "-q:v", "6", out_path], cwd=build)


def make_memo(build, out_path, text, extra=()):
    write_text(build, "f_memo.txt", text)
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "flite=textfile=f_memo.txt:voice=kal",
        "-ar", "16000", "-ac", "1"] + list(extra) + [out_path], cwd=build)


def make_letter(path, md):
    size, npages = build_pdf(parse(md), path)
    return size, npages


def main():
    for d in (CARE, ALT, EXPECTED):
        os.makedirs(d, exist_ok=True)

    missing = [f for f in FONTS if not os.path.exists(os.path.join(FONT_DIR, f))]
    if missing:
        raise SystemExit("Missing fonts in %s: %s" % (FONT_DIR, ", ".join(missing)))

    build = tempfile.mkdtemp(prefix="care-circle-demo-")
    for f in FONTS:
        shutil.copyfile(os.path.join(FONT_DIR, f), os.path.join(build, f))

    # --- the three readable labels -------------------------------------
    make_label(build, os.path.join(CARE, "01-label-amoxicillin.jpg"),
               "AMOXICILLIN", "500 mg capsules",
               "Take one capsule three times daily.",
               "Quantity:  84 capsules", "8841203", "08 November 2026",
               "Prescriber:  Dr A. Rahman", 11)
    make_label(build, os.path.join(CARE, "02-label-atorvastatin.jpg"),
               "ATORVASTATIN", "20 mg tablets",
               "Take one tablet once daily at night.",
               "Quantity:  28 tablets", "8841204", "08 November 2026",
               "Prescriber:  Dr A. Rahman", 29)
    make_label(build, os.path.join(CARE, "03-label-metformin.jpg"),
               "METFORMIN", "850 mg tablets",
               "Take one tablet twice daily with food.",
               "Quantity:  60 tablets", "8841205", "08 November 2026",
               "Prescriber:  Dr A. Rahman", 47)
    # A fourth label, blurred into the unreadable photo. It is NOT a copy of a
    # label already in the folder, so the dedupe step cannot collapse the pair.
    make_label(build, os.path.join(build, "src-unreadable.jpg"),
               "BENDROFLUMETHIAZIDE", "2.5 mg tablets",
               "Take one tablet once daily in the morning.",
               "Quantity:  28 tablets", "8841206", "08 November 2026",
               "Prescriber:  Dr A. Rahman", 63)

    # --- the deliberate unreadable image -------------------------------
    make_blurry(build, os.path.join(build, "src-unreadable.jpg"),
                os.path.join(CARE, "06-label-unreadable.jpg"))

    # --- the voice memo -------------------------------------------------
    memo = ("Hi, it's Margaret. I've been taking the new tablets since Tuesday. "
            "I felt a bit dizzy when I stood up this morning, and my ankle looks "
            "a little swollen. Should I keep taking the blood pressure tablet "
            "while I'm on the antibiotics? Also, can you ask the doctor whether "
            "the statin should be taken in the morning instead of at night? "
            "Thanks.")
    make_memo(build, os.path.join(CARE, "05-voice-memo-2026-11-06.wav"), memo)
    make_memo(build, os.path.join(ALT, "voice-memo.m4a"), memo,
              extra=["-c:a", "aac", "-b:a", "64k"])

    # --- the two letters ------------------------------------------------
    current = """# Clinic Letter - Outpatient Review

**Patient:** Margaret Ellison
**Date of appointment:** 08 November 2026
**Reporting doctor:** Dr A. Rahman, Consultant

## Diagnoses

Type 2 diabetes mellitus; hypertension; hyperlipidaemia (new).

## Current medications

Metformin 500 mg twice daily, continued.
Amlodipine 5 mg once daily, continued.
Atorvastatin 20 mg at night, started today.

## Results and measurements

HbA1c 6.9 percent (previous 7.1 percent).
Blood pressure 132/80 mmHg.
LDL cholesterol 3.4 mmol/L, new measurement.
eGFR 80 mL/min/1.73 m2.

## Findings

The patient reports feeling well. The family report one episode of dizziness on standing and a little ankle swelling; the patient is unsure whether it is new.

## Plan

Continue current medication. Review the family's questions at the next appointment.
"""
    previous = """# Clinic Letter - Outpatient Review

**Patient:** Margaret Ellison
**Date of appointment:** 12 May 2026
**Reporting doctor:** Dr A. Rahman, Consultant

## Diagnoses

Type 2 diabetes mellitus; hypertension.

## Current medications

Metformin 500 mg twice daily.
Amlodipine 5 mg once daily.

## Results and measurements

HbA1c 7.1 percent.
Blood pressure 138/84 mmHg.
eGFR 78 mL/min/1.73 m2.

## Findings

Stable. No new symptoms reported.

## Plan

Continue current medication. Repeat blood tests in six months.
"""
    make_letter(os.path.join(CARE, "04-clinic-letter-2026-11-08.pdf"), current)
    make_letter(os.path.join(CARE, "07-previous-report-2026-05-12.pdf"), previous)

    shutil.rmtree(build, ignore_errors=True)

    total = 0
    for base, _dirs, files in os.walk(OUT):
        for f in sorted(files):
            p = os.path.join(base, f)
            total += os.path.getsize(p)
            print("%9d  %s" % (os.path.getsize(p),
                               os.path.relpath(p, ROOT).replace("\\", "/")))
    print("----\n%d bytes total across %s" % (total, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
