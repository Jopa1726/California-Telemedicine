# WordPress integration kit — for the web developer

This folder lets you put the **"Doctors of Natural Medicine — California"** preview
into WordPress at `/california/` (and `/careers/california-physicians/`) **without
touching the existing Colorado site**. No zip hand-off, no personal data — everything
is in the GitHub repo.

> **The California service ships in LAUNCH MODE** (coming-soon + notify/physician
> inquiry only). It must not accept bookings or payments until the business flips to
> LIVE MODE with verified clinicians, entity, pricing, policies, and an approved
> clinical workflow. See `../docs/ASSUMPTIONS-AND-MISSING-FACTS.md`.

---

## You have two integration options. Start with Option 1 to see it live fast.

### Option 1 — Drop-in plugin (fastest, zero theme edits) ✅ recommended first step
A self-contained plugin (`dnm-california/`) serves the pre-built static pages inside
WordPress. It only owns `/california/*`, `/careers/california-physicians/*`, and
`/assets/*` — it never alters existing pages, posts, or the theme.

**Install:**
1. Clone the repo (or download it from GitHub → green **Code** button):
   `git clone https://github.com/Jopa1726/California-Telemedicine.git`
2. Copy the folder `wordpress/dnm-california/` into your WordPress
   `wp-content/plugins/` directory. (The built site is already inside it at
   `dnm-california/site/`.)
3. In **wp-admin → Plugins**, activate **"DNM California (Telemedicine Preview)."**
4. Go to **Settings → Permalinks** and click **Save Changes** once (flushes rewrite rules).
5. Visit **`https://YOURSITE/california/`** — the styled section loads.

**To update the content later:** edit `site.config.json` / `templates/` in the repo,
rebuild (`SITE_BASE_PATH="" python3 build.py`), copy `public/*` back into
`dnm-california/site/`, and redeploy the plugin folder. (A short script does this:
`wordpress/sync-build-into-plugin.sh`.)

> ⚠️ Asset paths: the plugin build uses **root-relative** paths (`/california/...`,
> `/assets/...`), which is correct when WordPress is at the **domain root**
> (`drnatmed.com`). If WordPress is installed in a subdirectory, rebuild with
> `SITE_BASE_PATH="/that-subdir"` and adjust the plugin's rewrite prefixes.

### Option 2 — Native theme integration (best long-term, more work)
Make the pages first-class, block-editor-editable WordPress pages. Full plan in
`../docs/INTEGRATION.md`:
- Recreate the shared chrome (`templates/partials/` header, state selector, launch
  banner, footer) in a **child theme** page template.
- Move each page's copy into WordPress pages or **ACF** fields; map
  `site.config.json` values (launch mode, pricing, physicians, policies, booking URLs,
  support contact) to fields so staff edit in wp-admin.
- Enqueue `assets/css/styles.css` + `assets/js/app.js` from the child theme.
- Add the "California (telemedicine)" item + state selector to the Colorado menu.
- Deactivate the Option 1 plugin once pages are native.

---

## What's in the repo (so you know what you're working with)
- `templates/` — hand-authored HTML page bodies + shared partials (the source of truth
  for markup).
- `site.config.json` — **single config** for copy, pricing, physicians, launch status,
  booking URLs, policies. Unknown facts are explicit `TODO_` placeholders — do not
  publish them as real claims.
- `build.py` — zero-dependency Python renderer. `SITE_BASE_PATH` controls the URL base.
- `public/` — a built copy (committed for convenience).
- `docs/` — audit, URL/brand architecture, SEO plan, measurement/privacy rules,
  assumptions + launch blockers, QA report.
- `.github/workflows/deploy-pages.yml` — the GitHub Pages preview deploy (unrelated to
  WordPress; safe to ignore for WP work).

## Important guardrails (please preserve)
- Keep **public forms minimal** (name/email only). Diagnoses, medical history, IDs, and
  consent belong in the approved **secure clinical system**, never a public form or email.
- **No analytics/advertising pixels or session replay** on clinical flows; never send
  PHI, form answers, documents, or sensitive URL params to analytics. See
  `../docs/MEASUREMENT-PRIVACY.md`.
- The booking buttons use a **demo adapter** that never confirms an appointment. Wire the
  approved, BAA-covered scheduling vendor before LIVE MODE.
- Keep **self-referencing canonicals** on California pages; do **not** canonicalize them to
  Colorado pages. Add the California sitemap to the WordPress sitemap.
- Don't modify production Colorado pages without written authorization.

## Questions the build already answers (point stakeholders here)
- URL map, canonicals, structured data, redirect policy → `../docs/ARCHITECTURE.md`
- What's missing before launch → `../docs/ASSUMPTIONS-AND-MISSING-FACTS.md`
- SEO preservation + content plan → `../docs/SEO-CONTENT-PLAN.md`
