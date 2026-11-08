# Disclosure and compliance

## Third-party components

The Skill is pure Markdown orchestration. It contains no executable code, no scripts, no binaries, no model weights and no external service calls. It has no runtime third-party dependencies.

The following development-time resource was used to author and statically check the Skill. It is not a runtime component and is not distributed inside the Skill package.

| Component | Source | Licence | Principal use |
|---|---|---|---|
| Uliya Skill Creation Tool (uliya-skill-kit) v0.7.3 | UGREEN Skill Developer Package | UGREEN developer licence, hackathon starter kit | Authoring the Skill and running the bundled static checker |

No third-party SDK, API, dataset or model is called at run time. No external service and no data flow leaves the NAS.

## Data handling

- All processing happens on the NAS. Medication photos, clinic letters and voice memos are read by the registered UGOS expert agents on the device.
- No health data is uploaded to any cloud service, and the Skill contains no code path that could upload it.
- The brief and the sibling update are written back to a folder on the NAS. Source files are tagged in place.
- The Skill never collects account numbers, credentials or contact details, and it never asks for them.

## Credentials and configuration

- The Skill contains no credentials, tokens, keys or passwords.
- No configuration file is required. The only inputs are the care folder, the parent name and the appointment date, all supplied by the user at run time.
- Folder paths are resolved at run time through the file expert. No path is hard-coded.

## Safety and scope

- The Skill organises and surfaces information only. It does not diagnose, does not advise on dosage, and does not replace a clinician.
- Every entry in the brief carries the file it came from, and every unreadable file is listed as unreadable.
- All write operations are approval-gated by the platform. The Skill never bypasses an approval, a permission or an audit step.
- The scope is the folder the user names. The Skill never widens the scope, never substitutes a similar folder and never invents a value that no delegated result contains.

## Intellectual property

The Skill and its core workflow were developed during the hackathon. No previously developed Skill or prior submission material is reused.
