# SawaTech × ASLM 2026: Implementation Notes

Package contents

| File | Purpose |
|---|---|
| `aslm-2026-preview.html` | Static, responsive review copy. The form is simulated, **not** live. |
| `elementor/sawatech-aslm2026-elementor.json` | Elementor template: Flexbox Containers + native widgets + Pro Form. |
| `elementor/custom-code-attribution-ga4.html` | Small Custom Code snippet: UTM → hidden fields, `generate_lead` on success. |
| `IMPLEMENTATION-NOTES.md` | This document. |

> **Import status (17 Nov 2026).** v2 was imported with Elementor's own importer (`wp elementor library import`) into a clean WordPress 6 + **free Elementor 4.4.1** install and rendered at 1366 px, 900 px and iPhone 13 widths: no errors, no placeholder images, no horizontal scroll. Not testable without a Pro licence: the Pro **Form** widget (it renders empty in free Elementor) and the **popup** template (free Elementor has no popup type). Import on staging first and check those two. Follow §0.

---

## 0. Importing the v2 templates (start here)

Order matters. The popup has to exist before the page's download button can point at it.

1. **Media Library:** upload `case-study/sawatech-case-study-clinical-trial-swahili.pdf`. If WordPress files it anywhere other than `/wp-content/uploads/2026/11/`, update `PDF_URL` in `tools/build_elementor.py`, re-run it, or edit the popup form's *Redirect* URL after import.
2. **Templates → Saved Templates → Import:** `elementor/sawatech-aslm2026-case-study-popup.json`. Then open it in Elementor and set:
   - **Email** action → *To* = the sales inbox. It's left blank on purpose.
   - **Publish → Conditions:** *Include → Singular → Page → ASLM 2026*. **Triggers:** none, because the button opens it.
3. **Templates → Saved Templates → Import:** `elementor/sawatech-aslm2026-elementor.json`. On the ASLM 2026 page: *Edit with Elementor → folder icon → My Templates → Insert*. Page Settings → Page Layout = **Elementor Canvas**.
   - The importer downloads every image (sawa-tech.com images plus the HIPAA/GDPR badges hosted on GitHub Pages) into the Media Library and links them by ID. Duplicates of existing media are expected, and you can delete the originals' copies later.
   - The hero's wave background is set in CSS and points at the existing `/2022/02/layered-waves-bg-03.svg`. WordPress blocks SVG uploads, so importing it would have produced a placeholder.
4. **Case-study button → popup:** select the *Download Full Case Study* button → Link → **Dynamic** (stack icon) → *Actions → Popup* → Action *Open Popup* → choose **ASLM 2026 – Case Study Download**. In the template it's a placeholder link (`#st-case-study-download`), because the popup's ID only exists after import.
5. **Consultation form:** set *Email → To* (sales inbox), as before (§4).
6. **Custom Code:** replace the old snippet with the updated `elementor/custom-code-attribution-ga4.html`. It now covers both forms.
7. **Page styles** live in an HTML widget named *"Page styles (keep at top)"* inside the header container. Don't delete it: the ribbon, flow connectors, process numbers, quote marks and logo sizing depend on it. Page-level Custom CSS is now empty.
8. **QA** with §8, plus: open the popup, submit it, confirm the PDF opens and the email arrives, then check Elementor → Submissions for both forms.

**Editing later:** change `tools/build_elementor.py` and re-run it rather than hand-editing the JSON, so both templates stay in sync with the preview.

---

## 1. Design-system audit (live sawa-tech.com, 17 Nov 2026)

Stack found in the page source: WordPress 7.1.4, **The7** theme (`dt-the7`), **Elementor 4.4 + Elementor Pro 4.4**, WP Rocket 3.24, Rank Math Pro, Maspik anti-spam (`contact-forms-anti-spam`), Safe SVG, WP WhatsApp Chat, **GTM container `GTM-KVVBWSC`**.

| Token | Live site (Elementor kit `post-9.css`) | Used on this page |
|---|---|---|
| Primary purple | `#4F2F6D` (`el_color_2`), most-used global | **`#4F2F6D`**, matching the live site. |
| Purple hover / press | n/a | `#5E3A80` / `#3F2557` (derived from `#4F2F6D`) |
| Light lavender surface | `#EDE4F5` (`el_color_2_3`) | `#EDE4F5` (same) |
| Accent | `#17BADD` cyan, `#FA8835` orange | `#FCB900` amber, sparingly (eyebrow + hero icons only) |
| Text | `#2C2C3A` / `#1D1D1B` | `#191919` headings, `#333333` body, `#5C5C5C` muted |
| Font | **Poppins** for all titles and body (DM Sans / Manrope loaded but barely used) | Poppins 400/500/600/700 |
| H1 / H2 scale | `el_title_1` 48/60 px, 700 (32 px mobile); `el_title_2` 40/52 px, 600 (28 px mobile) | H1 48 → 40 → 28; H2 40 → 32 → 26 |
| Body | `el_content_2` 16 px / 1.7, `el_content_1` 17 px / 1.7 | same |
| Card radius | 15 px (most common radius on the site) | 15 px |
| Buttons | Pill, 100 px radius; white-on-purple hero buttons with purple text | same |
| Shadows | `0 0 20px rgba(0,0,0,.1)` to `.15` | `0 0 20px rgba(0,0,0,.08–.12)` |
| Container | Boxed, 1100–1300 px variants (theme box width 1280) | 1200 px boxed, 24 px gutters (16 px mobile) |
| Breakpoints | Elementor defaults: 1024 / 767 | same |
| Hero pattern | Purple band + `layered-waves-bg-03.svg`, cut-out portrait on the right | same pattern |
| "Why choose" pattern | Solid purple cards with white icon + white title | reused for §4 |
| Footer | Purple band (`el_color_2_2`) | purple band, simplified |

**Colour decision (resolved).** The page uses the live site's purple `#4F2F6D` rather than the brand-guideline `#663694`, so it matches sawa-tech.com exactly. The hero artwork still uses the lighter guideline purple, which sits against the darker hero background as a secondary shade. White text on `#4F2F6D` measures about 11:1, which passes WCAG AA and AAA.

**Global Colors / Fonts.** The primary purple and lavender already exist as live globals: `el_color_2` (`#4F2F6D`) and `el_color_2_3` (`#EDE4F5`). After import, link those widgets to them with the globe icon. The JSON uses hex values so it imports cleanly on any kit. For the remaining values, add custom globals (Site Settings → Global Colors → Custom):
`ST Primary Hover #5E3A80`, `ST Primary Press #3F2557`, `ST Amber #FCB900`, `ST Text #191919`, `ST Body #333333`, `ST Muted #5C5C5C`, `ST Off-white #F5F5F5`. Typography can link to the existing Poppins globals (`el_title_1`, `el_title_2`, `el_content_2`).

---

## 2. Visual assets reused (all verified HTTP 200 on 17 Nov 2026)

| Use | URL | In Media Library already? |
|---|---|---|
| Logo (white), header + footer | `https://sawa-tech.com/wp-content/uploads/2020/11/sawatech-Logo-WHITE.png` | Yes |
| Hero image (African clinician, purple/amber, transparent WebP, 1200×1200, 331 KB) | `https://sawa-tech.com/wp-content/uploads/2025/08/1-Healthcare-Translation-Services-That-Put-Patient-Safety-First.webp` | Yes (healthcare industry page) |
| Hero background waves | `https://sawa-tech.com/wp-content/uploads/2022/02/layered-waves-bg-03.svg` | Yes (homepage hero) |
| ISO 17100 badge | `https://sawa-tech.com/wp-content/uploads/2025/11/iso-17100-2015.webp` | Yes |
| ISO 9001 badge | `https://sawa-tech.com/wp-content/uploads/2025/11/iso-9001-2015.webp` | Yes |
| ISO 18587 badge | `https://sawa-tech.com/wp-content/uploads/2025/11/iso-18587-2017.webp` | Yes |
| Favicon | `https://sawa-tech.com/wp-content/uploads/2025/11/cropped-sawatech-favicon-32x32.webp` | Yes (site icon) |

Icons are Font Awesome 5 (bundled with Elementor): `file-medical`, `flask`, `microchip`, `users`, `globe-africa`, `user-md`, `award`, `cogs`, `arrow-down`, `arrow-right`, `calendar`, `map-marker-alt`, `check-circle`. No third-party icon packs.

Alternates on the site, if marketing wants a different hero:
`/2025/08/Sawatechs-Life-Sciences-Translation-Services.webp` (but it has baked-in text and a quote, so it's not recommended), `/2025/08/Clinical-trial-translation.webp`, `/2025/08/Medical-device-translation-1.webp`, `/2025/08/7-Clinical-documentation.webp`.

### Media Library actions
1. **Re-select every image from the Media Library after import.** The template references them by URL with `id: ""`. Re-selecting attaches the attachment ID, so `srcset` / responsive sizes and **alt text** work.
2. **Set alt text** in the Media Library: hero = "Healthcare professional in a white coat holding a clipboard, representing accurate healthcare translation"; logo = "SawaTech"; the ISO badges already have good alt text.
3. **Optimise the hero.** 331 KB is heavy for an LCP image on mobile. Export a 1000 px version under about 120 KB (WebP q≈75). Set the image widget to Medium-Large, or use the `-768x768` size on mobile.
4. **Company-profile PDF.** Its images couldn't be extracted here (no PDF renderer on this machine). Nothing on the page depends on it. If marketing wants profile visuals such as the "Global Footprint" map, export them as WebP from the source design file and upload them.

---

## 3. WordPress admin settings to complete

1. **Import:** Templates → Saved Templates → Import → `sawatech-aslm2026-elementor.json`. Create Page "ASLM 2026", slug **`aslm-2026`**, Edit with Elementor → folder icon → My Templates → Insert.
2. **Page layout:** the template sets *Elementor Canvas* so the full site header and mega-footer are removed (the page has its own minimal header and footer). Confirm GTM still loads on Canvas pages: View Source, then search `GTM-KVVBWSC`.
3. **Privacy Policy link ⚠:** `https://sawa-tech.com/privacy-policy/` currently **301-redirects to `/terms-and-conditions/`**. Publish a real Privacy Policy page (or fix the redirect) **before launch**. The form's consent text and the footer both link to `/privacy-policy/`.
4. **Rank Math** (page → Rank Math panel):
   - SEO title: `SawaTech at ASLM 2026 | Life Sciences Localization`
   - Meta description: `Meet SawaTech at ASLM 2026. Explore clinical research, laboratory, medical device, and healthcare localization solutions for African markets.`
   - Canonical: `https://sawa-tech.com/aslm-2026/`. Index / follow.
   - Schema: none (no FAQ, review or event schema). Don't add speculative markup.
   - Open Graph image: reuse the hero, or `/2026/10/sawatech-social-share-1200x630-1.webp`.
5. **WP Rocket:** keep the defaults. utm_* parameters are already served from cache, which is why the attribution script runs client-side. Exclude nothing. Make sure "Delay JavaScript execution" does not delay jQuery or the Custom Code snippet. If it's on, add `st_aslm2026_attr` to the delay-JS exclusions.
6. **Hide the WhatsApp chat bubble on this page** (WP WhatsApp Chat → display rules) to keep a single conversion action.
7. **Spam:** Maspik is active and supports Elementor forms. Also keep the honeypot field included in the template. If reCAPTCHA v3 keys are configured (Elementor → Settings → Integrations), you can add a reCAPTCHA v3 field.

---

## 4. Form widget configuration (already in the JSON; verify after import)

- **Form Name:** SawaTech ASLM 2026 · **Form ID (Additional Options):** `sawatech_aslm2026`

| Field ID | Type | Label | Required | Width (desktop/mobile) |
|---|---|---|---|---|
| `full_name` | Text | Full Name | ✔ | 50 / 100 |
| `business_email` | Email | Business Email | ✔ | 50 / 100 |
| `organization` | Text | Company / Organization | ✔ | 100 |
| `service_need` | Select | What Do You Need? | ✔ | 100 |
| `project_details` | Textarea (4 rows) | Brief Project Details (optional) | n/a | 100 |
| `utm_source` `utm_medium` `utm_campaign` `utm_content` `utm_term` | Hidden | n/a | n/a | n/a |
| `lead_source` | Hidden | `booth_qr` / source / `direct` | n/a | n/a |
| `landing_page` | Hidden | page URL without query | n/a | n/a |
| `privacy_consent` | Acceptance | consent text + Privacy Policy link | ✔ | 100 |
| `hp_check` | Honeypot | n/a | n/a | n/a |

Select options (first line is an empty-value placeholder, so "required" blocks submission):
```
Select an option|
Clinical Research Translation
Laboratory & Medical Documentation
Medical Device Localization
Patient / Public Health Communication
Other Localization Requirements
```

- **Actions After Submit:** *Collect Submissions* + *Email*. Add *Webhook* only if a CRM endpoint exists (see below).
- **Email:** To = **[SawaTech sales inbox, which the admin sets; left blank in the template on purpose]** · Subject `New ASLM 2026 enquiry: [field id="service_need"]` · Message `[all-fields]` (includes the UTM fields) · From name "SawaTech Website" · From email = an address on the sawa-tech.com domain (SPF/DKIM) · Reply-To `[field id="business_email"]` · Meta data: date, time, page URL. **Don't include Remote IP.**
- **Messages (custom):** Success: "Thank you for contacting SawaTech. Our team has received your request and will be in touch." Error: "Sorry, something went wrong and your request was not sent. Please try again or email support@sawa-tech.net." No redirect after submit, and no extra CTA.
- **CRM (optional):** Webhook action → the CRM's inbound URL. Store the URL only in the Elementor action field, never in page content. For HubSpot / Zoho / Salesforce, prefer their native Elementor integrations or a middleware (Zapier/Make) so no secrets sit in WordPress.
- **Submissions:** Elementor → Submissions, filtered by form "SawaTech ASLM 2026". Set a retention period in line with the privacy policy.

---

## 4b. Case-study download pop-up (gated PDF)

The case-study section's **Download Full Case Study** button opens a pop-up form. The PDF is delivered only after a successful submission. This isn't in the JSON template yet, so build it in Elementor Pro:

1. **Media Library:** upload `case-study/sawatech-case-study-clinical-trial-swahili.pdf` (from this repo). Copy its URL. The cover page names the client (Merck); SawaTech confirmed on 17 Nov 2026 that this is cleared for public use.
2. **Templates → Popups → Add New:** name it "ASLM 2026 – Case Study Download".
   - Layout: width 560 px, height fit to content, position centre, close button on, overlay `rgba(30,17,42,.62)`, border radius 15 px. Entrance animation: Fade In.
   - Content: a purple header (gradient `#3F2557 → #4F2F6D → #5E3A80`), an amber badge "Free case study · PDF", an H2 "Get the Full Case Study" and the one-line summary. Then the Form widget below.
   - **Conditions:** none (opened by the button only). **Triggers:** none. **Advanced:** check *Avoid multiple popups*.
3. **Form widget** inside the pop-up: Form Name `SawaTech Case Study Download`, Form ID `sawatech_case_study`.

| Field ID | Type | Label | Required | Width (desktop/mobile) |
|---|---|---|---|---|
| `first_name` | Text | First Name | ✔ | 50 / 100 |
| `last_name` | Text | Last Name | ✔ | 50 / 100 |
| `business_email` | Email | Business Email | ✔ | 100 |
| `company` | Text | Company | ✔ | 50 / 100 |
| `phone` | Tel | Phone Number (placeholder `+27 21 300 1810`) | ✔ | 50 / 100 |
| `utm_source` `utm_medium` `utm_campaign` `lead_source` | Hidden | n/a | n/a | n/a |
| `lead_type` | Hidden | default value `case_study_download` | n/a | n/a |
| `privacy_consent` | Acceptance | "I agree that SawaTech may store and use my details to send this case study and follow up about relevant services, as described in the Privacy Policy." | ✔ | 100 |
| `hp_check` | Honeypot | n/a | n/a | n/a |

   - Submit button: "Download the Case Study", full width, primary purple.
   - **Actions After Submit:** *Collect Submissions* + *Email* (To: sales inbox · Subject `Case study download: [field id="company"]` · Reply-To `[field id="business_email"]`) + **Redirect** to the PDF URL from step 1. Optionally add *Email 2* to the visitor with the PDF link, so they keep a copy.
   - Success message: "Thank you! Your case study download is starting."
4. **Button link:** on the case-study section's "Download Full Case Study" button, set Link → Dynamic → *Actions → Popup → Open Popup → "ASLM 2026 – Case Study Download"*.
5. **Tracking:** the updated `elementor/custom-code-attribution-ga4.html` fills the hidden fields when the pop-up opens and sends `generate_lead` with `form_id: sawatech_case_study` and `lead_type: case_study_download`. In GA4, register `lead_type` as a custom dimension, so case-study leads are reported separately from consultation requests.

**Note:** gating stops casual downloads, not determined ones. The PDF URL is public once someone has it. That's acceptable for marketing content. For true restriction, send the PDF only by email (Email 2 action) and leave out the Redirect.

---

## 5. Campaign tracking

**URLs** (one page, different parameters):

| Channel | URL |
|---|---|
| Booth QR | `https://sawa-tech.com/aslm-2026/?utm_source=aslm2026&utm_medium=qr&utm_campaign=aslm2026` |
| LinkedIn (paid) | `…/aslm-2026/?utm_source=linkedin&utm_medium=paid_social&utm_campaign=aslm2026` |
| Email outreach | `…/aslm-2026/?utm_source=email&utm_medium=outreach&utm_campaign=aslm2026` |
| Google Ads | `…/aslm-2026/?utm_source=google&utm_medium=cpc&utm_campaign=aslm2026` (or rely on auto-tagging) |

Use `utm_content` to tell placements apart (e.g. `booth_banner`, `table_card`, `badge_scan`) without new designs.

**How it works.** `custom-code-attribution-ga4.html` is added once via Elementor → Custom Code (End of body, Priority 10, condition: this page only). It:
1. Reads the five UTM parameters from the URL. If they're absent, it reuses the values stored earlier in the same browser tab (sessionStorage).
2. Writes them into the hidden fields, plus `lead_source` (`booth_qr` when `utm_medium=qr`) and `landing_page`.
3. Listens for Elementor Pro's `submit_success` event on the form with id `sawatech_aslm2026`. Only then does it push `{event:'generate_lead', form_id, lead_source, utm_source, utm_medium, utm_campaign}` to `dataLayer`. Button clicks never fire a conversion, and **no name, email, company or free text is sent to analytics.**

**GTM setup (container GTM-KVVBWSC):**
1. Data Layer Variables: `form_id`, `lead_source`, `utm_source`, `utm_medium`, `utm_campaign`.
2. Trigger: Custom Event `generate_lead`, condition `form_id equals sawatech_aslm2026`.
3. Tag: GA4 Event, name `generate_lead`, parameters `form_id`, `lead_source`. Mark `generate_lead` as a Key Event in GA4. Optionally fire LinkedIn Insight and Google Ads conversion tags on the same trigger.
4. Verify in GTM Preview: submit a test lead, then confirm exactly one `generate_lead` event.

---

## 6. Missing information needed before publication

1. **Clinical-trial case study:** the PDF wasn't attached in this session. Metrics are taken verbatim from the brief (800,000 words; 1.5 months; 100% reported on-time delivery; memoQ; Swahili; TEP). **Marketing must check them against the signed-off case study.** The client stays anonymous ("a leading global healthcare organization").
2. **ASLM-edition revised copy and life-sciences profile:** not attached. The copy follows the brief exactly.
3. **Booth number / exhibitor status:** none shown on the page. Add it only once confirmed, as text in the hero icon list (e.g. "Booth B12, CTICC").
4. **Sales inbox** for notifications, plus the **From** address.
5. **Privacy Policy page** (see §3.3) and the consent wording, approved by whoever owns data protection (POPIA for South African visitors; GDPR if EU visitors).
6. **Brand colour:** resolved. The page uses the live `#4F2F6D`. If the site is later rebranded to the guideline `#663694`, update the `el_color_2` global and the hex values on this page together.
7. **CRM** target and field mapping, if any.

Verified facts used: ISO 17100, ISO 9001, ISO 18587 (company profile + site badges); HQ South Africa, hub in Bahrain, since 2013 (profile, not shown on the page); public contact `support@sawa-tech.net` (site + profile); ASLM 2026 = 8–11 December 2026, CTICC, Cape Town (aslm2026.org). Client logos (IQVIA, Molina, etc.) appear on the site but are **deliberately not used**, so no client endorsement is implied.

---

## 7. Elementor build specification (fallback if import fails)

All boxed containers: Content Width = Boxed, 1200 px; Padding 96/24 (desktop), 72/24 (tablet), 56/16 (mobile); Gap 24. Headings: Poppins. Section H2: `#4F2F6D`, 600, 40/32/26 px, line-height 1.3, centred.

```
Page (Elementor Canvas, title hidden)
├─ C0 Header  [Container, Row, boxed, bg #3F2557, space-between, pad 18/24]
│   ├─ Image: logo white, 168px (140 mobile), link https://sawa-tech.com/
│   └─ Button: "Discuss Your Localization Needs" → #discuss, small, white bg / purple text, radius 100, hidden on mobile
├─ C1 Hero  [Container, Row → Column on mobile, bg #3F2557 + layered-waves-bg-03.svg cover,
│            gradient overlay #2E1B40→#3F2557 100°, opacity .88, pad 48/24/72 (mobile 24/16/40), gap 40]
│   ├─ C1a [Column, 55% / 100%, gap 18]
│   │   ├─ Heading <p>: "SAWATECH AT ASLM 2026", 13px 600 uppercase, ls 1.6px, #FCB900
│   │   ├─ Heading H1: "Clear Communication. Stronger Health Outcomes Across Africa." white, 700, 48/40/28
│   │   ├─ Text Editor: supporting copy, rgba(255,255,255,.88), 17/15.5px
│   │   ├─ Icon List (inline): calendar "ASLM 2026 | 8–11 December" · map-marker "Cape Town, South Africa"; icons #FCB900, text white 15px 500
│   │   └─ Button: CTA → #discuss, lg, white bg, #4F2F6D text, hover bg #EDE4F5, radius 100, pad 16/32, icon arrow-down right, full width on mobile
│   └─ C1b [Column, 45% / 100%, align end → centre on mobile]
│       └─ Image: hero WebP, width 500px (200px mobile)
├─ C2 Capabilities [boxed, white]
│   ├─ Heading H2 + Text Editor intro (#5C5C5C, 17px, max-width 780 via .st-measure)
│   └─ C2g [Row, wrap, gap 24 / 16]
│       └─ 4 × Card [Column, 25% / 50% tablet / 100% mobile, white, border 1px #E3E3E3, radius 15, shadow 0 0 20 .08, pad 28/24]
│           └─ Icon Box: stacked square icon, bg #4F2F6D, icon white 26px, radius 14, position top (left on mobile), title H3 19px 600 #191919, desc 15px #5C5C5C
├─ C3 Proof [boxed, bg #EDE4F5]
│   ├─ Heading H2 "800,000 Words. One Critical Timeline." + Heading <p> "Clinical Trial Localization into Swahili" 20px 500 #191919
│   ├─ C3m [Row → Column mobile, gap 24 / 12]
│   │   └─ 3 × Metric [Column (Row on mobile), 33.3% / 100%, bg #4F2F6D, radius 15, pad 32/24]
│   │       ├─ Heading <p> value: 52/44/34px 700 white   ("800,000" · "1.5 months" · "100%")
│   │       └─ Heading <p> label: 16px 500 white 88%     ("words localized" · "delivery timeline" · "reported on-time delivery")
│   ├─ Text Editor: case-study copy, centred (left on mobile), max-width 780
│   ├─ C3w [Row → Column mobile, centred, gap 12]: Button(non-link, outline 2px #4F2F6D, white, radius 100) × 4 with Icon arrow-right between (rotated 90° on mobile)
│   └─ Text Editor: "Client name withheld for confidentiality." 13px #5C5C5C
├─ C4 Why SawaTech [boxed, white]
│   ├─ Heading H2
│   ├─ C4g [Row, wrap]: 4 × Card, bg #4F2F6D, shadow .12, Icon Box with icon bg rgba(255,255,255,.14), text white / 88%
│   ├─ C4i [Row, centred, gap 28]: 3 × Image ISO badges, 96px (76 mobile)
│   └─ Text Editor: certification disclaimer, 13px #5C5C5C
├─ C5 Form [boxed, Row → Column on tablet, bg #F5F5F5, CSS ID = discuss, gap 56]
│   ├─ C5a [Column 42% / 100%]: Heading H2 (left), Text Editor, Icon List (check-circle, 2 items)
│   └─ C5b [Column 58% / 100%, white, radius 15, top border 4px #4F2F6D, shadow 0 0 30 .10, pad 36 (22/18 mobile)]
│       ├─ Form (see §4). Fields: bg white, border 1px #BDBDBD, radius 8; labels 14px 500 #191919; button #4F2F6D → hover #5E3A80, radius 100, full width
│       └─ Text Editor: privacy notice 12.5px #5C5C5C
└─ C6 Footer [boxed, Row → Column mobile, bg #4F2F6D, space-between, pad 36/24]
    ├─ Image: logo white 150px
    ├─ Icon List (inline, no icons): sawa-tech.com · support@sawa-tech.net · Privacy Policy; white, hover #FCB900
    └─ Container (100%, top border 1px rgba(255,255,255,.2)) → Text Editor "© 2026 SawaTech. All rights reserved."
```

**Custom CSS** (Page Settings → Advanced → Custom CSS; already in the JSON, under 10 lines):
`.st-measure` max-width, the form-field focus ring, visible `:focus-visible` outlines (black, white on purple), the non-clickable workflow chips, and smooth scrolling with a reduced-motion override.

Class names in use: `st-header`, `st-hero`, `st-capabilities`, `st-proof`, `st-metric`, `st-workflow`, `st-step`, `st-why`, `st-card(--dark)`, `st-form-section`, `st-form-card`, `st-footer`, `st-measure`.

---

## 8. Pre-launch QA checklist

- [ ] Every CTA (header, hero, form submit) has the same label; header and hero scroll to `#discuss`
- [ ] Exactly one H1; H2 per section; card titles H3
- [ ] Mobile (375 px): hero CTA visible without scrolling; no horizontal scroll; form fields full width
- [ ] Test lead from the QR URL: email arrives with `utm_medium = qr`, `lead_source = booth_qr`; submission appears in Elementor → Submissions
- [ ] GTM Preview shows one `generate_lead` per successful submit and none on a failed or empty submit
- [ ] Privacy Policy link resolves to a privacy policy, not to Terms
- [ ] WhatsApp bubble hidden on this page
- [ ] Lighthouse mobile: LCP under 2.5 s after hero optimisation; Accessibility ≥ 95
- [ ] Case-study figures signed off against the source PDF
