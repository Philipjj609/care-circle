#!/usr/bin/env python3
"""Dependency-free renderer: care-circle Round 1 proposal -> PDF, and the pretest Skill ZIP."""
import os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPOSAL_MD = os.path.join(ROOT, "proposal", "care-circle-proposal.md")
SKILL_DIR = os.path.join(ROOT, "skill", "care-circle")
DIST = os.path.join(ROOT, "dist")

PAGE_W, PAGE_H = 595.28, 841.89          # A4 portrait, points
MARGIN_L = MARGIN_R = 56.0
MARGIN_T = 64.0
MARGIN_B = 60.0
BODY_SIZE = 10.5
LEADING = 14.5

# Helvetica widths per 1000 units (approximation of the standard AFM metrics)
_W = {c: 556 for c in range(32, 127)}
for _c, _w in {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667, "'": 191,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 278, ';': 278, '<': 584, '=': 584, '>': 584, '?': 556,
    '@': 1015, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469, '_': 556,
    '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556,
    'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556,
    'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722,
    'x': 500, 'y': 500, 'z': 500, '{': 334, '|': 260, '}': 334, '~': 584,
}.items():
    _W[ord(_c)] = _w
_WB = dict(_W)
for _c in 'ilmfjt.,:;\'!|/()[]{} ':
    _WB[ord(_c)] = max(_WB.get(ord(_c), 556), 320)
for _c in 'mwMW@_':
    _WB[ord(_c)] = 1000
for _c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    _WB[ord(_c)] = min(1000, int(_WB.get(ord(_c), 667) * 1.06))
for _c in '0123456789':
    _WB[ord(_c)] = 556


def width(s, size, bold=False):
    tbl = _WB if bold else _W
    return sum(tbl.get(ord(ch), 556) for ch in s) * size / 1000.0


def wrap(text, size, max_w, bold=False):
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = w if not cur else cur + ' ' + w
        if width(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or ['']


def esc(s):
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')


def build_pdf(blocks, path):
    max_w = PAGE_W - MARGIN_L - MARGIN_R
    pages, page = [], []

    def new_page():
        nonlocal page
        if page:
            pages.append(page)
        page = []

    y = [MARGIN_T]

    def ensure(need):
        if y[0] + need > PAGE_H - MARGIN_B:
            new_page()
            y[0] = MARGIN_T

    for kind, text in blocks:
        if kind == 'h1':
            ensure(30)
            y[0] += 8
            page.append(('text', text, 17, True, MARGIN_L, PAGE_H - y[0]))
            y[0] += 24
        elif kind == 'h2':
            ensure(26)
            y[0] += 8
            page.append(('text', text, 12, True, MARGIN_L, PAGE_H - y[0]))
            y[0] += 19
        elif kind == 'hr':
            ensure(14)
            y[0] += 4
            page.append(('rule', MARGIN_L, PAGE_H - y[0], PAGE_W - MARGIN_R))
            y[0] += 10
        elif kind == 'meta':
            ensure(18)
            page.append(('text', text, 10.5, True, MARGIN_L, PAGE_H - y[0]))
            y[0] += 16
        else:
            for ln in wrap(text, BODY_SIZE, max_w):
                ensure(LEADING)
                page.append(('text', ln, BODY_SIZE, False, MARGIN_L, PAGE_H - y[0]))
                y[0] += LEADING
            y[0] += 4
    if page:
        pages.append(page)

    objects = []
    font_reg = 3
    font_bold = 4
    page_start = 5

    # object 1 catalog, 2 pages (filled later), 3/4 fonts
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"")  # placeholder for pages
    objects.append(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
                    "/Encoding /WinAnsiEncoding >>").encode())
    objects.append(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
                    "/Encoding /WinAnsiEncoding >>").encode())

    page_ids = []
    for pg in pages:
        content = []
        for item in pg:
            if item[0] == 'text':
                _, s, size, bold, x, yy = item
                font = "/F2" if bold else "/F1"
                content.append(
                    f"BT {font} {size:.2f} Tf 1 0 0 1 {x:.2f} {yy:.2f} Tm ({esc(s)}) Tj ET"
                )
            else:
                _, x1, yy, x2 = item
                content.append(
                    f"0.8 w {x1:.2f} {yy:.2f} m {x2:.2f} {yy:.2f} l S"
                )
        stream = "\n".join(content).encode('cp1252', 'replace')
        content_id = len(objects) + 2
        objects.append(("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] "
                        "/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> "
                        "/Contents %d 0 R >>" % (PAGE_W, PAGE_H, font_reg, font_bold,
                                                content_id)).encode())
        objects.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
        page_ids.append(content_id - 1)

    objects[1] = ("<< /Type /Pages /Kids [%s] /Count %d >>" %
                  (" ".join("%d 0 R" % i for i in page_ids), len(page_ids))).encode()

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += ("%d 0 obj\n" % i).encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += ("xref\n0 %d\n" % (len(objects) + 1)).encode()
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += ("%010d 00000 n \n" % off).encode()
    out += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" %
            (len(objects) + 1, xref_pos)).encode()
    with open(path, 'wb') as fh:
        fh.write(bytes(out))
    return len(out), len(pages)


def parse(md):
    blocks = []
    for raw in md.split('\n'):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith('# '):
            blocks.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            blocks.append(('h2', line[3:].strip()))
        elif re.match(r'^---+$', line.strip()):
            blocks.append(('hr', ''))
        elif re.match(r'^\*\*(.+):\*\*\s*(.*)$', line):
            m = re.match(r'^\*\*(.+):\*\*\s*(.*)$', line)
            blocks.append(('meta', m.group(1) + ': ' + m.group(2)))
        else:
            blocks.append(('p', re.sub(r'\*\*(.+?)\*\*', r'\1', line)))
    return blocks


def main():
    os.makedirs(DIST, exist_ok=True)
    md = open(PROPOSAL_MD, encoding='utf-8').read()
    pdf_path = os.path.join(DIST, "care-circle-proposal.pdf")
    size, npages = build_pdf(parse(md), pdf_path)
    print("PDF: %s (%d bytes, %d page(s))" % (pdf_path, size, npages))

    zip_path = os.path.join(DIST, "care-circle-pretest-skill.zip")
    files = [
        ("care-circle/SKILL.md", os.path.join(SKILL_DIR, "SKILL.md")),
        ("care-circle/references/workflow-matrix.md",
         os.path.join(SKILL_DIR, "references", "workflow-matrix.md")),
        ("care-circle/references/disclosure-and-compliance.md",
         os.path.join(SKILL_DIR, "references", "disclosure-and-compliance.md")),
    ]
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc, src in files:
            z.write(src, arc)
    total = sum(os.path.getsize(s) for _, s in files)
    print("ZIP: %s (%d bytes, %d files, %d bytes uncompressed)" %
          (zip_path, os.path.getsize(zip_path), len(files), total))


if __name__ == '__main__':
    main()
