# Doctors of Natural Medicine — California (Expansion Preview)

A polished, dependency‑free static website for the proposed California telemedicine
service **"Doctors of Natural Medicine — California"**, designed to live at
`https://drnatmed.com/california/` within the existing WordPress brand.

> **Status: PREVIEW / NOT PUBLISHED.** This is a build preview only. Nothing here
> modifies the live Colorado WordPress site. The California service ships in
> **LAUNCH MODE** by default (coming‑soon + notify/physician inquiry) and must not
> accept clinical bookings or payments until the business flips to LIVE MODE with
> verified clinicians, entity, pricing, policies, and an approved clinical workflow.

---

## Why this stack

The sandbox used to build this has **no access to the npm registry** (403) and
cannot run WordPress. A framework build (Astro/Vite/React) was therefore not
possible. The deliverable is intentionally a **zero‑dependency static site**:

- Semantic, server‑rendered HTML — fully search‑readable with JS disabled.
- Modern CSS (one stylesheet, custom properties for the brand palette).
- A tiny amount of progressive‑enhancement vanilla JS (state selector, nav,
  launch‑mode form behavior, reduced‑motion‑aware reveals).
- All copy, pricing, physician, policy and launch‑status values live in
  **`site.config.json`** so non‑engineers can edit them, and so unknown facts stay
  as explicit `TODO:` placeholders instead of invented claims.

This output ports cleanly into WordPress (the HTML/partials map to a child‑theme
template + a few ACF fields) or can be hosted as a static section behind a reverse
proxy at `/california/`. See `docs/INTEGRATION.md`.

## Run the preview locally

```bash
cd drnatmed-california
python3 build.py        # renders site.config.json + templates -> ./public
python3 -m http.server 8080 --directory public
# open http://localhost:8080/california/
```

`build.py` is a ~200‑line, standard‑library‑only renderer (no pip installs). It
injects shared head/header/footer, the config values, and the launch‑mode flag
into each page so there is a single source of truth.

## What's in here

| Path | Purpose |
|---|---|
| `site.config.json` | **Single source of truth** for copy variables, pricing, physicians, policies, launch status, analytics config. Edit this. |
| `build.py` | Standard‑library static renderer + dev server helper. |
| `templates/` | Page bodies + shared partials (head, header, footer). |
| `public/` | Generated output (what you deploy). Also committed so it can be viewed without a build. |
| `public/assets/` | CSS, JS, SVG logo/illustrations (all original, no third‑party scripts). |
| `docs/AUDIT.md` | Current‑site + competitor audit with dated sources. |
| `docs/ARCHITECTURE.md` | Brand + URL map, canonicals, sitemap, structured data, redirect policy. |
| `docs/INTEGRATION.md` | How to mount under `/california/` in WordPress or via proxy; booking + forms integration plan. |
| `docs/SEO-CONTENT-PLAN.md` | Colorado SEO preservation + California content plan. |
| `docs/ASSUMPTIONS-AND-MISSING-FACTS.md` | Documented assumptions, conflicting live‑site claims, and the blocking facts needed before LIVE MODE. |
| `docs/MEASUREMENT-PRIVACY.md` | Analytics events + the sensitive‑data exclusion rules. |
| `docs/QA-REPORT.md` | What was tested and what remains unverified. |

## Deploy authorization

Do **not** publish or touch production Colorado pages without explicit written
deployment authorization from the business. See `docs/ASSUMPTIONS-AND-MISSING-FACTS.md`.
