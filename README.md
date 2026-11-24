# SawaTech × ASLM 2026: Landing Page

Conversion landing page for SawaTech's participation in ASLM 2026 (8–11 December 2026, CTICC, Cape Town).

| File | What it is |
|---|---|
| `aslm-2026-preview.html` | Static, responsive review copy. Open it in a browser. The form is simulated. |
| `elementor/sawatech-aslm2026-elementor.json` | Elementor page template v2: hero, trust band (ISO / HIPAA / GDPR + client logos), capabilities, case study with request-to-result flow, process, why-us, testimonials, consultation form, footer. |
| `elementor/sawatech-aslm2026-hero.json` | Hero section only (container template) for swapping the hero on an existing page. |
| `elementor/sawatech-aslm2026-case-study-popup.json` | Elementor Pro **popup** template: case-study download form (`sawatech_case_study`) that redirects to the PDF. |
| `case-study/sawatech-case-study-clinical-trial-swahili.pdf` | The full case study. Upload it to the WordPress Media Library. |
| `tools/build_elementor.py` | Generates both JSON templates. Edit it, not the JSON, then run `python3 tools/build_elementor.py`. |
| `tools/build_static.py` | Rebuilds `docs/` (GitHub Pages) and `_artifact/` from the preview. |
| `elementor/custom-code-attribution-ga4.html` | Elementor Custom Code snippet: UTM → hidden fields, GA4 `generate_lead` on successful submit. |
| `IMPLEMENTATION-NOTES.md` | Design audit, assets, WordPress admin settings, form and tracking setup, build spec, QA checklist. |

Target URL: `https://sawa-tech.com/aslm-2026/`

**To build it in WordPress, start with §0 of `IMPLEMENTATION-NOTES.md`** (import order, popup link, settings to fill in).

## Online review copy

`_artifact/` is the version of the preview published as a private claude.ai artifact
(https://claude.ai/artifact/MPMDgptewTjxDLYgEX1iRJ). The images are bundled locally because the artifact viewer blocks images from other sites.
Republish it from `_artifact/index.html` with the same `assets/` files.
