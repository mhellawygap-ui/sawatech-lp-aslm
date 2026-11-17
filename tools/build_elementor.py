#!/usr/bin/env python3
"""Generate the Elementor Pro templates for the SawaTech × ASLM 2026 page.

Outputs
  elementor/sawatech-aslm2026-elementor.json        page template (v2)
  elementor/sawatech-aslm2026-case-study-popup.json popup template (case-study download)

Input
  tools/elementor_base_v1.json  the original v1 template. Header, hero, capability
  cards, why-cards, consultation form and footer are reused from it so their tuned
  settings carry over; everything else is built here. Re-running is idempotent.

Native widgets only (container, heading, text-editor, image, icon, icon-box,
icon-list, button, image-carousel, testimonial, html, Pro form). Styling that
Elementor controls can't express lives in one HTML widget (<style>) at the top
of the page, so it works without Pro's per-page Custom CSS.

Usage:  python3 tools/build_elementor.py
"""
import copy, itertools, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = json.loads((ROOT / "tools" / "elementor_base_v1.json").read_text())
UP = "https://sawa-tech.com/wp-content/uploads/"
MEDIA = "https://mhellawygap-ui.github.io/sawatech-lp-aslm/elementor-media/"  # importer downloads these
PDF_URL = UP + "2026/11/sawatech-case-study-clinical-trial-swahili.pdf"

P, P_HOVER, P_PRESS, P_TINT = "#4F2F6D", "#5E3A80", "#3F2557", "#EDE4F5"
AMBER, INK, BODY, MUTED, BORDER, OFF = "#FCB900", "#191919", "#333333", "#5C5C5C", "#E3E3E3", "#F5F5F5"

_ids = (f"5a{n:05x}" for n in itertools.count(1))
def uid():
    return next(_ids)

# ---------------------------------------------------------------- helpers
def px(size): return {"unit": "px", "size": size, "sizes": []}
def pct(size): return {"unit": "%", "size": size, "sizes": []}
def em(size): return {"unit": "em", "size": size, "sizes": []}
def box(t, r=None, b=None, l=None, unit="px"):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l),
            "isLinked": len({t, r, b, l}) == 1}
def gap(n): return {"column": str(n), "row": str(n), "isLinked": True, "unit": "px", "size": n}
def font(size, weight="400", lh=1.6, tablet=None, mobile=None, prefix="typography", **extra):
    s = {f"{prefix}_typography": "custom", f"{prefix}_font_family": "Poppins",
         f"{prefix}_font_weight": str(weight), f"{prefix}_font_size": px(size),
         f"{prefix}_line_height": em(lh)}
    if tablet: s[f"{prefix}_font_size_tablet"] = px(tablet)
    if mobile: s[f"{prefix}_font_size_mobile"] = px(mobile)
    for k, v in extra.items(): s[f"{prefix}_{k}"] = v
    return s

def container(children, inner=True, **s):
    s.setdefault("content_width", "full")
    s.setdefault("padding", box(0))
    return {"id": uid(), "elType": "container", "isInner": inner, "settings": s, "elements": children}

def grid(children, cols, tablet=None, mobile=1, gap_px=24, **s):
    s.update({"container_type": "grid",
              "grid_columns_grid": {"unit": "fr", "size": cols, "sizes": []},
              "grid_columns_grid_tablet": {"unit": "fr", "size": tablet or cols, "sizes": []},
              "grid_columns_grid_mobile": {"unit": "fr", "size": mobile, "sizes": []},
              "grid_rows_grid": {"unit": "fr", "size": 1, "sizes": []},
              "grid_gaps": gap(gap_px), "grid_auto_flow": "row"})
    return container(children, **s)

def section(children, cls, bg=None, **s):
    s.update({"content_width": "boxed", "boxed_width": px(1200), "flex_direction": "column",
              "flex_gap": gap(24),
              "padding": box(96, 24, 96, 24), "padding_tablet": box(72, 24, 72, 24),
              "padding_mobile": box(56, 16, 56, 16), "html_tag": "section", "css_classes": cls})
    if bg: s.update({"background_background": "classic", "background_color": bg})
    return container(children, inner=False, **s)

def widget(kind, **s):
    return {"id": uid(), "elType": "widget", "widgetType": kind, "isInner": False, "settings": s, "elements": []}

def heading(text, tag="h2", color=INK, align="center", **typo):
    return widget("heading", title=text, header_size=tag, align=align, title_color=color, **typo)

def h2(text, eid=None):
    w = heading(text, "h2", P, **font(40, "600", 1.3, tablet=32, mobile=26))
    if eid: w["settings"]["_element_id"] = eid
    return w

def lead(text, align="center", color=MUTED, size=17, cls="st-measure"):
    return widget("text-editor", editor=f"<p>{text}</p>", align=align, text_color=color,
                  _css_classes=cls, **font(size, lh=1.7, mobile=15.5))

def image(url, alt, width=None, cls="", **s):
    s.update({"image": {"url": url, "id": "", "source": "library", "alt": alt}, "image_size": "full"})
    if width: s["width"] = width
    if cls: s["_css_classes"] = cls
    return widget("image", **s)

def fa(name, lib="fa-solid"): return {"value": name, "library": lib}

# --------------------------------------------------------------- base parts
IDX = {}
def _index(e):
    IDX[e["id"]] = e
    for c in e.get("elements", []): _index(c)
for e in BASE["content"]: _index(e)
def base(eid): return copy.deepcopy(IDX[eid])

# ------------------------------------------------------------------ styles
CSS = r"""
/* SawaTech × ASLM 2026 — page styles that Elementor controls can't express. */
.st-measure{max-width:780px;margin-inline:auto}
.elementor-field-group .elementor-field:focus{border-color:#4F2F6D;box-shadow:0 0 0 3px rgba(79,47,109,.25)}
a:focus-visible,.elementor-button:focus-visible{outline:3px solid #191919;outline-offset:3px}
.st-hero a:focus-visible,.st-footer a:focus-visible,.st-result a:focus-visible{outline-color:#fff}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.st-hero h1{max-width:22ch}
.st-hero{background-image:url("https://sawa-tech.com/wp-content/uploads/2022/02/layered-waves-bg-03.svg");background-position:center;background-size:cover;background-repeat:no-repeat}

/* trust band */
.st-trust .st-badge img{max-height:62px;width:auto;object-fit:contain;margin-inline:auto}
@media (max-width:767px){.st-trust .st-badge img{max-height:46px}
  .st-badges>:last-child:nth-child(odd){grid-column:1 / -1;justify-self:center;width:calc(50% - 7px)}}
.st-logos .swiper-slide-image{height:100px;width:150px;object-fit:contain;mix-blend-mode:multiply;margin-inline:auto}
@media (max-width:767px){.st-logos .swiper-slide-image{height:78px;width:116px}}

/* case study: corner ribbon */
.st-case{position:relative;overflow:visible}
.st-ribbon-wrap{position:absolute!important;top:-10px;left:-10px;width:200px!important;height:200px;z-index:3;pointer-events:none}
.st-ribbon{position:absolute;inset:0;overflow:hidden}
.st-ribbon::before,.st-ribbon::after{content:"";position:absolute;z-index:-1;display:block;border:5px solid #3F2557;border-top-color:transparent;border-left-color:transparent}
.st-ribbon::before{top:0;right:0}
.st-ribbon::after{bottom:0;left:0}
.st-ribbon span{position:absolute;right:-34px;top:52px;width:300px;padding:11px 0;transform:rotate(-45deg);background:linear-gradient(90deg,#3F2557,#4F2F6D 30%,#5E3A80 70%,#3F2557);box-shadow:0 6px 12px rgba(0,0,0,.18);color:#fff;font:600 12.5px/1 "Poppins",sans-serif;letter-spacing:.1em;text-transform:uppercase;text-align:center}
@media (max-width:767px){.st-ribbon-wrap{width:150px!important;height:150px}.st-ribbon span{width:230px;right:-28px;top:37px;font-size:10px;letter-spacing:.07em;padding:8px 0}}

/* case study: fact chips */
.st-chips ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.st-chips li{background:#EDE4F5;color:#191919;border-radius:100px;padding:7px 16px;font-size:13.5px;line-height:1.3}
.st-chips b{color:#4F2F6D;font-weight:600;margin-right:6px}
@media (max-width:767px){.st-chips li{font-size:12.5px;padding:6px 12px;border-radius:14px}}

/* case study: request-to-result flow */
.st-flow{counter-reset:stflow}
.st-flow-step .elementor-widget-icon{position:relative}
.st-flow-step .elementor-icon{position:relative}
.st-flow-step .elementor-icon::after{counter-increment:stflow;content:counter(stflow);position:absolute;top:-4px;right:-4px;width:24px;height:24px;border-radius:50%;background:#4F2F6D;color:#fff;font:600 12px/24px "Poppins",sans-serif;text-align:center;box-shadow:0 0 0 3px #fff}
@media (min-width:1025px){
  .st-flow-step:not(:last-child) .elementor-widget-icon::after{content:"";position:absolute;top:34px;left:calc(50% + 44px);right:calc(-50% + 22px);height:2px;background:linear-gradient(90deg,#4F2F6D 0 55%,transparent 0) 0 0/10px 2px repeat-x}
  .st-flow-step:not(:last-child) .elementor-widget-icon::before{content:"";position:absolute;top:29px;right:calc(-50% + 18px);border:6px solid transparent;border-left:8px solid #4F2F6D}
}
@media (max-width:1024px){
  .st-flow-step>.e-con{flex:1 1 0!important;min-width:0;width:auto!important;--width:auto}
  .st-flow-step:not(:last-child) .elementor-widget-icon{align-self:stretch}
  .st-flow-step:not(:last-child) .elementor-widget-icon::after{content:"";position:absolute;top:76px;bottom:-22px;left:33px;width:2px;background:linear-gradient(#4F2F6D 0 55%,transparent 0) 0 0/2px 10px repeat-y}
  @media (max-width:767px){.st-flow-step:not(:last-child) .elementor-widget-icon::after{top:60px;left:25px}}
}

/* case study: result panel */
.st-result{position:relative;overflow:hidden}
.st-result::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;border:30px solid rgba(255,255,255,.06);pointer-events:none}
.st-result-tag .elementor-heading-title{display:inline-flex;align-items:center;gap:8px;background:#FCB900;border-radius:100px;padding:6px 14px}
.st-result-tag .elementor-heading-title::before{content:"✓";font-weight:700}
@media (min-width:1025px){.st-metric+.st-metric{border-left:1px solid rgba(255,255,255,.2);padding-left:20px!important}}
.st-result-checks{border-top:1px solid rgba(255,255,255,.2);padding-top:20px}

/* process timeline */
.st-process{counter-reset:stproc}
.st-proc-step{position:relative;padding-left:76px!important}
.st-proc-step::before{counter-increment:stproc;content:counter(stproc,decimal-leading-zero);position:absolute;left:0;top:0;width:56px;height:56px;border-radius:50%;background:#4F2F6D;color:#fff;display:grid;place-items:center;font:600 17px/1 "Poppins",sans-serif;box-shadow:0 0 0 6px #EDE4F5}
.st-proc-step:last-child::before{background:#FCB900;color:#191919;box-shadow:0 0 0 6px #FFF3CC}
.st-proc-step:not(:last-child)::after{content:"";position:absolute;left:27px;top:62px;bottom:-22px;width:2px;background:linear-gradient(#4F2F6D 0 50%,transparent 0) 0 0/2px 10px repeat-y}
@media (max-width:767px){.st-proc-step{padding-left:60px!important}.st-proc-step::before{width:44px;height:44px;font-size:15px;box-shadow:0 0 0 4px #EDE4F5}.st-proc-step:not(:last-child)::after{left:21px;top:50px}}

/* testimonials */
.st-quote .elementor-testimonial-content::before{content:"\201C";display:block;font:700 64px/0.9 Georgia,serif;color:#4F2F6D;margin-bottom:8px}
.st-quote--accent .elementor-testimonial-content::before{color:#FCB900}
.st-quote .elementor-widget-testimonial{flex-grow:1;display:flex;flex-direction:column}
.st-quote .elementor-widget-testimonial>*{flex-grow:1}
.st-quote .elementor-testimonial-wrapper{display:flex;flex-direction:column;height:100%}
.st-quote .elementor-testimonial-content{flex:1}
.st-quote .elementor-testimonial-meta{border-top:1px solid #E3E3E3;padding-top:20px;margin-top:24px}
.st-quote--accent .elementor-testimonial-meta{border-top-color:rgba(255,255,255,.2)}
.st-quote .elementor-testimonial-image img{background:#EDE4F5}

/* media splits: hide decorative images on phones */
@media (max-width:767px){.st-split-media{display:none!important}}
"""

def styles():
    return widget("html", html=f"<style>{CSS.strip()}</style>", _title="Page styles (keep at top)",
                  _position="absolute", _element_width="initial", _element_custom_width=px(0),
                  _offset_x=px(0), _offset_y=px(0))

# ------------------------------------------------------------------ sections
def header():
    h = base("1a2b3c2")
    h["elements"].insert(0, styles())
    return h

def hero():
    h = base("1a2b3cd")
    # SVG background: WordPress blocks SVG uploads by default, so the importer would swap in a
    # placeholder. Reference the file already on sawa-tech.com from CSS instead (see CSS .st-hero).
    for k in ("background_image", "background_position", "background_repeat", "background_size"):
        h["settings"].pop(k, None)
    text_col, media_col = h["elements"]
    text_col["settings"]["width"] = pct(62)
    media_col["settings"]["width"] = pct(38)
    for w in text_col["elements"]:
        s = w["settings"]
        if w.get("widgetType") == "heading" and s.get("header_size") == "h1":
            s.update(font(46, "700", 1.2, tablet=40, mobile=27, letter_spacing_mobile=px(-0.4)))
        if w.get("widgetType") == "text-editor":
            s["editor"] = ("<p>Accurate, culturally appropriate multilingual content for clinical research, "
                           "laboratory and patient communications across Africa and the Middle East.</p>")
            s["typography_font_size_mobile"] = px(14.5)
    return h

def badge(url, alt):
    return container([image(url, alt, cls="st-badge", align="center")],
                     flex_direction="column", flex_justify_content="center",
                     min_height=px(84), min_height_mobile=px(66),
                     padding=box(10, 14), padding_mobile=box(8),
                     background_background="classic", background_color="#FFFFFF",
                     border_border="solid", border_width=box(1), border_color=BORDER,
                     border_radius=box(15))

LOGOS = [("2025/10/New-Project-20.png", "IQVIA"), ("2025/10/New-Project-8.png", "PATH"),
         ("2025/10/New-Project-13.png", "Humana"), ("2025/10/New-Project-18.png", "Anthem"),
         ("2025/10/New-Project-17.png", "Molina Healthcare"), ("2025/10/New-Project-15.png", "Sandata"),
         ("2025/10/New-Project-12.png", "LifeWorks"),
         ("2025/10/New-Project-5.png", "Bloomberg Center for Cities at Harvard University"),
         ("2025/10/New-Project-9.png", "Samsung"), ("2025/10/New-Project-1.png", "Huawei"),
         ("2025/10/New-Project-2.png", "Meta"), ("2025/10/New-Project-6.png", "OpenAI")]

def trust():
    label = widget("text-editor",
                   editor='<p><strong>Certified quality.</strong><br><span style="color:#4F2F6D;font-weight:600">Secure, compliant handling.</span></p>',
                   text_color=INK, align="left", align_tablet="center",
                   **font(15, "600", 1.45))
    badges = grid([
        badge(UP + "2025/11/iso-17100-2015.webp", "ISO 17100:2015 certified — translation services"),
        badge(UP + "2025/11/iso-9001-2015.webp", "ISO 9001:2015 certified — quality management"),
        badge(UP + "2025/11/iso-18587-2017.webp", "ISO 18587:2017 certified — machine translation post-editing"),
        badge(MEDIA + "badge-hipaa-compliant.png", "HIPAA-compliant handling of health information"),
        badge(MEDIA + "badge-gdpr-compliant.png", "GDPR-compliant personal data handling"),
    ], 5, tablet=5, mobile=2, gap_px=14, css_classes="st-badges")
    certs = container([label, badges], flex_direction="row", flex_direction_tablet="column",
                      flex_align_items="center", flex_gap=gap(32), flex_gap_tablet=gap(16))
    label["settings"]["_element_width"] = "initial"
    label["settings"]["_element_custom_width"] = px(190)
    label["settings"]["_element_width_tablet"] = "inherit"
    badges["settings"]["flex_grow"] = 1
    badges["settings"]["width"] = pct(100)
    note = widget("text-editor",
                  editor="<p>ISO certifications cover language services; they are not clinical, laboratory or regulatory accreditation.</p>",
                  align="right", align_tablet="center", text_color=MUTED, **font(12, lh=1.5))
    clients_head = heading("Trusted by leading healthcare, research &amp; global organizations", "p", MUTED,
                           **font(14, "500", 1.4, mobile=12, text_transform="uppercase", letter_spacing=px(1.1)))
    carousel = widget("image-carousel",
                      carousel=[{"id": "", "url": UP + p, "alt": a, "source": "library"} for p, a in LOGOS],
                      thumbnail_size="full", slides_to_show="6", slides_to_show_tablet="4",
                      slides_to_show_mobile="3", slides_to_scroll="1", navigation="none",
                      image_stretch="no", link_to="none", caption_type="",
                      autoplay="yes", pause_on_hover="yes", pause_on_interaction="yes",
                      autoplay_speed=2200, infinite="yes", effect="slide", speed=700,
                      image_spacing="custom", image_spacing_custom=px(28),
                      _css_classes="st-logos")
    clients = container([clients_head, carousel], flex_direction="column", flex_gap=gap(14),
                        padding=box(28, 0, 0, 0), padding_mobile=box(20, 0, 0, 0),
                        border_border="solid", border_width=box(1, 0, 0, 0), border_color=BORDER)
    return container([certs, note, clients], inner=False, content_width="boxed", boxed_width=px(1200),
                     flex_direction="column", flex_gap=gap(12),
                     padding=box(40, 24, 36, 24), padding_mobile=box(28, 16, 28, 16),
                     border_border="solid", border_width=box(0, 0, 1, 0), border_color=BORDER,
                     html_tag="section", css_classes="st-trust",
                     _title="Trust band: certifications + client logos")

def split(media, content, media_first=True, media_pct=42):
    media_c = container([media], width=pct(media_pct), width_tablet=pct(100),
                        flex_direction="column", flex_justify_content="center",
                        css_classes="st-split-media")
    content_c = container([content], width=pct(100 - media_pct), width_tablet=pct(100),
                          flex_direction="column")
    kids = [media_c, content_c] if media_first else [content_c, media_c]
    return container(kids, flex_direction="row", flex_direction_tablet="column",
                     flex_align_items="center", flex_gap=gap(48), flex_gap_tablet=gap(32))

def cards_grid(card_ids):
    cards = []
    for cid in card_ids:
        c = base(cid)
        for k in ("width", "width_tablet", "width_mobile"): c["settings"].pop(k, None)
        cards.append(c)
    return grid(cards, 2, tablet=2, mobile=1, gap_px=20)

def capabilities():
    s = base("1a2b3d9")
    head, sub, _old = s["elements"]
    s["settings"]["background_background"] = "classic"
    s["settings"]["background_color"] = OFF
    media = image(UP + "2025/08/2-Why-Inaccurate-Healthcare-Translation-Puts-Everyone-at-Risk-768x512.webp",
                  "Doctor presenting multilingual healthcare documents and patient-communication icons",
                  image_border_radius=box(15))
    s["elements"] = [head, sub, split(media, cards_grid(["1a2b3d1", "1a2b3d3", "1a2b3d5", "1a2b3d7"]))]
    return s

FLOW = [
    ("fas fa-file-alt", "The Request", "800,000 words of clinical trial content into Swahili, due in 1.5 months."),
    ("fas fa-database", "Centralized Setup", "One memoQ workflow with shared translation memories, termbases and client-approved style guides."),
    ("fas fa-users", "Specialist Team", "20+ Swahili professionals: translators, editors, QA specialists, a PM and a localization engineer."),
    ("fas fa-layer-group", "Layered TEP", "Translation, editing and proofreading layers running in parallel."),
    ("fas fa-chart-line", "Daily Governance", "Daily production tracking, real-time query resolution and continuous quality control."),
]

def flow_step(icon, title, text):
    return container([
        widget("icon", selected_icon=fa(icon), view="stacked", shape="circle", align="center",
               align_tablet="left", primary_color=P_TINT, secondary_color=P,
               size=px(28), size_mobile=px(22), icon_padding=px(20), icon_padding_mobile=px(15),
               _element_width_tablet="initial", _element_custom_width_tablet=px(68),
               _element_width_mobile="initial", _element_custom_width_mobile=px(52),
               _flex_size_tablet="none", _flex_size_mobile="none"),
        container([
            heading(title, "h3", INK, align="center", align_tablet="left", **font(16.5, "600", 1.35, mobile=16)),
            widget("text-editor", editor=f"<p>{text}</p>", align="center", align_tablet="left",
                   text_color=MUTED, **font(14, lh=1.6)),
        ], flex_direction="column", flex_gap=gap(6), padding_tablet=box(6, 0, 0, 0),
           _flex_size_tablet="grow", _flex_size_mobile="grow"),
    ], flex_direction="column", flex_direction_tablet="row", flex_direction_mobile="row",
       flex_wrap="nowrap", flex_wrap_tablet="nowrap", flex_wrap_mobile="nowrap",
       flex_gap=gap(16), flex_gap_tablet=gap(18), flex_gap_mobile=gap(14),
       padding_tablet=box(0, 0, 22, 0), css_classes="st-flow-step")

def metric(value, unit, label):
    title = value + (f'<small style="font-size:.48em;font-weight:600;margin-left:4px">{unit}</small>' if unit else "")
    return container([
        heading(title, "p", "#FFFFFF", align="left", **font(44, "700", 1.1, tablet=40, mobile=32)),
        heading(label, "p", "rgba(255,255,255,0.88)", align="left", **font(14.5, "400", 1.4, mobile=13)),
    ], flex_direction="column", flex_gap=gap(6), css_classes="st-metric")

def case_study():
    ribbon = widget("html", html='<div class="st-ribbon" aria-hidden="true"><span>Client Case Study</span></div>',
                    _css_classes="st-ribbon-wrap", _title="Corner ribbon")
    chips = widget("text-editor", _css_classes="st-chips", editor=(
        '<ul aria-label="Project overview">'
        "<li><b>Client</b>Leading global healthcare organization</li>"
        "<li><b>Service</b>Translation, editing &amp; proofreading</li>"
        "<li><b>Language</b>Swahili</li><li><b>Platform</b>memoQ</li></ul>"))
    flow_label = heading("From request to result", "p", MUTED,
                         **font(13, "600", 1.4, text_transform="uppercase", letter_spacing=px(1.6)))
    flow = grid([flow_step(*f) for f in FLOW], 5, tablet=1, mobile=1, gap_px=20, css_classes="st-flow",
                padding=box(10, 0, 0, 0))
    flow["settings"]["grid_gaps_tablet"] = gap(0)
    down = widget("icon", selected_icon=fa("fas fa-arrow-down"), view="default", align="center",
                  primary_color=P, size=px(26))
    tag = heading("The result", "p", INK, align="left", _css_classes="st-result-tag",
                  **font(12.5, "700", 1, text_transform="uppercase", letter_spacing=px(1.2)))
    metrics = grid([metric("800,000", "", "words successfully localized"),
                    metric("1.5", "months", "from kickoff to final delivery"),
                    metric("100%", "", "on-time delivery"),
                    metric("20+", "", "language professionals coordinated")],
                   4, tablet=2, mobile=2, gap_px=20)
    checks = widget("icon-list", view="inline", _css_classes="st-result-checks",
                    icon_list=[{"_id": uid(), "text": t, "selected_icon": fa("fas fa-check")} for t in
                               ("Consistent terminology across all deliverables", "Full adherence to quality requirements")],
                    icon_color=AMBER, text_color="#FFFFFF", icon_size=px(16), space_between=px(28),
                    **font(14.5, lh=1.5, mobile=13.5, prefix="icon_typography"))
    result = container([tag, metrics, checks], flex_direction="column", flex_gap=gap(22),
                       padding=box(32, 36), padding_mobile=box(24, 20),
                       background_background="gradient", background_color=P_PRESS,
                       background_color_b=P_HOVER, background_gradient_angle={"unit": "deg", "size": 120, "sizes": []},
                       border_radius=box(15), css_classes="st-result")
    button = widget("button", text="Download Full Case Study",
                    link={"url": "#st-case-study-download", "is_external": "", "nofollow": "", "custom_attributes": ""},
                    align="center", align_mobile="justify", size="lg",
                    selected_icon=fa("fas fa-download"), icon_align="left", icon_indent=px(10),
                    button_css_id="cta-case-study",
                    button_text_color=P, background_color="rgba(0,0,0,0)",
                    hover_color="#FFFFFF", button_background_hover_color=P,
                    border_border="solid", border_width=box(2), border_color=P,
                    border_radius=box(100), text_padding=box(14, 30),
                    **font(16, "600", 1.2))
    meta = widget("text-editor", editor="<p>Free · PDF · 4 pages · 1.5 MB</p>", align="center",
                  text_color=MUTED, **font(13, lh=1.4))
    cta = container([button, meta], flex_direction="row", flex_direction_mobile="column",
                    flex_justify_content="center", flex_align_items="center", flex_gap=gap(20),
                    flex_gap_mobile=gap(8), padding=box(8, 0, 0, 0))
    card = container([
        ribbon,
        h2("800,000 Words. One Critical Timeline."),
        heading("Clinical Trial Localization into Swahili", "p", INK, **font(20, "500", 1.4, mobile=17)),
        chips, flow_label, flow, down, result, cta,
    ], flex_direction="column", flex_gap=gap(20),
       padding=box(64, 56, 52, 56), padding_tablet=box(56, 32, 40, 32), padding_mobile=box(84, 18, 28, 18),
       background_background="classic", background_color="#FFFFFF", border_radius=box(15),
       box_shadow_box_shadow_type="yes",
       box_shadow_box_shadow={"horizontal": 0, "vertical": 10, "blur": 40, "spread": 0, "color": "rgba(63,37,87,0.12)"},
       css_classes="st-case", html_tag="article")
    return section([card], "st-proof", bg=P_TINT, _title="Case study")

STEPS = [("Inquiry & Order", "Define requirements, language pairs, deadlines and any regulatory or confidentiality needs."),
         ("Assignment", "Select the best native linguists and subject experts for clinical, laboratory or device content."),
         ("Translation & Localization", "Accurate, culturally adapted content built on approved glossaries and translation memories."),
         ("Quality Assurance (QA)", "Multi-step TEP review: translation, editing and proofreading by separate linguists."),
         ("Final Delivery", "On-time, ISO-compliant, ready-to-use files in the formats you need.")]

def process():
    steps = container([
        container([heading(t, "h3", INK, align="left", **font(19, "600", 1.35, mobile=17)),
                   widget("text-editor", editor=f"<p>{d}</p>", align="left", text_color=MUTED, **font(15, lh=1.65))],
                  flex_direction="column", flex_gap=gap(4), min_height=px(56), css_classes="st-proc-step")
        for t, d in STEPS], flex_direction="column", flex_gap=gap(26), flex_gap_mobile=gap(20),
        css_classes="st-process")
    media = image(UP + "2025/10/Process-Section-Visuals-03-1.webp",
                  "SawaTech project manager presenting a project dashboard on a laptop")
    return section([h2("How We Work: From Brief to Final Delivery"),
                    lead("A clear, structured approach to ensure quality and impact."),
                    split(media, steps, media_first=False, media_pct=42)], "st-process-section",
                   _title="Process")

def why():
    s = base("1a2b400")
    head = s["elements"][0]
    s["settings"]["background_background"] = "classic"
    s["settings"]["background_color"] = OFF
    cards = cards_grid(["1a2b3f3", "1a2b3f5", "1a2b3f7", "1a2b3f9"])
    certified = cards["elements"][2]["elements"][0]["settings"]
    certified["title_text"] = "Certified & Secure"
    certified["description_text"] = ("ISO 17100, 9001 and 18587 certified workflows, with HIPAA- and "
                                     "GDPR-compliant handling of sensitive data.")
    media = image(UP + "2025/08/3-Healthcare-Translation-Services-Built-on-Accuracy-and-Compliance-768x512.webp",
                  "Clinician reviewing digital medical records, representing accurate and compliant healthcare translation")
    s["elements"] = [head, split(media, cards)]
    return s

QUOTES = [
    ("They translated our EMA dossier and cleaned the layout for submission. Zero formatting issues, and terminology aligned perfectly with our reference list.",
     "Sara Haddad", "Regulatory Affairs Manager, Pharma", "2023/05/woman-02.webp", False),
    ("Our patient-facing materials needed sensitivity and clarity. Sawatech tested terminology with local clinicians and adapted visuals for literacy levels—impactful and respectful.",
     "Aisha Bello", "Program Director, NGO (Health)", "2023/05/woman-02.webp", True),
    ("We handed Sawatech 1,200 pages of manuals. They built a termbase, standardized units, and returned clean InDesign files ready for print. Our field techs noticed the difference.",
     "David Stein", "Technical Documentation Lead, Industrial Automation", "2023/05/man02.webp", False),
]

def testimonial(text, name, job, img, accent):
    w = widget("testimonial", testimonial_content=text, testimonial_name=name, testimonial_job=job,
               testimonial_image={"url": UP + img, "id": "", "source": "library", "alt": ""},
               testimonial_image_size="full", testimonial_image_position="aside", testimonial_alignment="left",
               content_content_color="rgba(255,255,255,0.88)" if accent else BODY,
               name_text_color="#FFFFFF" if accent else INK,
               job_text_color="rgba(255,255,255,0.75)" if accent else MUTED,
               image_size=px(52),
               **font(15.5, lh=1.7, mobile=15, prefix="content_typography"),
               **font(15.5, "600", 1.35, prefix="name_typography"),
               **font(13.5, lh=1.45, prefix="job_typography"))
    s = dict(flex_direction="column", padding=box(32, 28, 28, 28), padding_mobile=box(24, 20, 22, 20),
             background_background="classic", background_color=P if accent else "#FFFFFF",
             border_border="solid", border_width=box(1), border_color=P if accent else BORDER,
             border_radius=box(15), box_shadow_box_shadow_type="yes",
             box_shadow_box_shadow={"horizontal": 0, "vertical": 0, "blur": 20, "spread": 0, "color": "rgba(0,0,0,0.08)"},
             css_classes="st-quote" + (" st-quote--accent" if accent else ""))
    return container([w], **s)

def testimonials():
    return section([h2("What Our Clients Say"),
                    lead("Regulatory, public-health and technical teams rely on SawaTech for content where accuracy matters."),
                    grid([testimonial(*q) for q in QUOTES], 3, tablet=1, mobile=1, gap_px=24)],
                   "st-testimonials", _title="Testimonials")

def page():
    out = copy.deepcopy(BASE)
    out["title"] = "SawaTech × ASLM 2026 — Landing Page (v2)"
    out["page_settings"]["custom_css"] = ""   # styles now live in the HTML widget (works with or without Pro CSS)
    out["content"] = [header(), hero(), trust(), capabilities(), case_study(), process(), why(),
                      testimonials(), base("1a2b418"), base("1a2b420")]
    return out

# ------------------------------------------------------------------ popup
def popup():
    fields = [
        dict(custom_id="first_name", field_type="text", field_label="First Name", required="true", width="50", width_mobile="100"),
        dict(custom_id="last_name", field_type="text", field_label="Last Name", required="true", width="50", width_mobile="100"),
        dict(custom_id="business_email", field_type="email", field_label="Business Email", required="true", width="100"),
        dict(custom_id="company", field_type="text", field_label="Company", required="true", width="50", width_mobile="100"),
        dict(custom_id="phone", field_type="tel", field_label="Phone Number", required="true", width="50", width_mobile="100",
             placeholder="+27 21 300 1810"),
        dict(custom_id="utm_source", field_type="hidden", field_label="utm_source", field_value=""),
        dict(custom_id="utm_medium", field_type="hidden", field_label="utm_medium", field_value=""),
        dict(custom_id="utm_campaign", field_type="hidden", field_label="utm_campaign", field_value=""),
        dict(custom_id="lead_source", field_type="hidden", field_label="lead_source", field_value=""),
        dict(custom_id="lead_type", field_type="hidden", field_label="lead_type", field_value="case_study_download"),
        dict(custom_id="privacy_consent", field_type="acceptance", field_label="Consent", required="true", width="100",
             show_label="", acceptance_text=('I agree that SawaTech may store and use my details to send this case study '
                                             'and follow up about relevant services, as described in the '
                                             '<a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>.')),
        dict(custom_id="hp_check", field_type="honeypot", field_label="Leave empty"),
    ]
    for f in fields: f["_id"] = uid()
    base_form = IDX["1a2b40f"]["settings"]
    style = {k: copy.deepcopy(v) for k, v in base_form.items() if k not in (
        "form_name", "form_id", "form_fields", "button_text", "button_css_id", "submit_actions", "email_subject",
        "success_message", "email_to", "email_reply_to", "row_gap")}
    form = widget("form", **style, form_name="SawaTech Case Study Download", form_id="sawatech_case_study",
                  form_fields=fields, button_text="Download the Case Study", button_css_id="cta-case-study-submit",
                  selected_button_icon=fa("fas fa-download"), button_icon_align="left", button_icon_indent=px(8),
                  submit_actions=["save-to-database", "email", "redirect"],
                  email_to="", email_subject='Case study download: [field id="company"]',
                  email_reply_to='[field id="business_email"]', redirect_to=PDF_URL,
                  success_message="Thank you! Your case study download is starting.",
                  row_gap=px(14))
    head = container([
        heading("Free case study · PDF", "p", INK, align="left", _css_classes="st-gate-badge",
                **font(11.5, "700", 1, text_transform="uppercase", letter_spacing=px(0.9))),
        heading("Get the Full Case Study", "h2", "#FFFFFF", align="left", **font(26, "600", 1.3, mobile=22)),
        widget("text-editor", editor="<p>How SawaTech localized 800,000 words of clinical trial content into Swahili in "
                                     "1.5 months, with 100% on-time delivery.</p>",
               align="left", text_color="rgba(255,255,255,0.88)", **font(14.5, lh=1.6)),
    ], flex_direction="column", flex_gap=gap(10), padding=box(30, 56, 26, 32), padding_mobile=box(24, 48, 20, 20),
       background_background="gradient", background_color=P_PRESS, background_color_b=P_HOVER,
       background_gradient_angle={"unit": "deg", "size": 120, "sizes": []})
    gate_css = widget("html", html=("<style>.st-gate-badge .elementor-heading-title{display:inline-block;"
                                    "background:#FCB900;border-radius:100px;padding:5px 12px}</style>"),
                      _title="Popup styles")
    body = container([form], flex_direction="column", padding=box(24, 32, 28, 32), padding_mobile=box(20))
    root = container([gate_css, head, body], inner=False, flex_direction="column", flex_gap=gap(0),
                     css_classes="st-gate", _title="Case-study download popup")
    return {
        "version": "0.4",
        "title": "ASLM 2026 – Case Study Download",
        "type": "popup",
        "page_settings": {
            "width": px(560), "width_mobile": {"unit": "vw", "size": 92, "sizes": []},
            "height_type": "fit_to_content", "content_position": "top",
            "horizontal_position": "center", "vertical_position": "center",
            "close_button_position": "inside", "close_button_color": "#FFFFFF",
            "close_button_hover_color": "#EDE4F5", "icon_size": px(20),
            "entrance_animation": "fadeIn", "entrance_animation_duration": {"unit": "px", "size": 0.25, "sizes": []},
            "background_background": "classic", "background_color": "#FFFFFF",
            "border_radius": box(15),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal": 0, "vertical": 24, "blur": 60, "spread": 0, "color": "rgba(25,15,35,0.35)"},
            "overlay_background_background": "classic", "overlay_background_color": "rgba(30,17,42,0.62)",
            "avoid_multiple_popups": "yes", "prevent_scroll": "yes",
        },
        "content": [root],
    }

def main():
    (ROOT / "elementor" / "sawatech-aslm2026-elementor.json").write_text(
        json.dumps(page(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "elementor" / "sawatech-aslm2026-case-study-popup.json").write_text(
        json.dumps(popup(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote page + popup templates")

if __name__ == "__main__":
    main()
