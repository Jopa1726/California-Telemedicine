# Integration plan

How this preview becomes a live `/california/` section, and how booking, forms,
and analytics connect — honestly, without over-claiming.

## 1. Mounting under `drnatmed.com/california/`

The current site is WordPress. Two supported paths; pick based on hosting:

### Option A — Port into the WordPress theme (recommended if WP can carry it)
- Create a child-theme **page template** (`page-california.php` / block templates) that
  reproduces the header, state selector, launch banner, and footer partials in
  `templates/partials/`.
- Move the per-page copy into WordPress pages (or a few **ACF/Custom Fields**) so staff edit
  content in wp-admin. Map `site.config.json` values to ACF fields:
  launch mode, pricing published + amounts, physician list, policy text, booking URLs, support contact.
- Enqueue `assets/css/styles.css` and `assets/js/app.js` from the child theme.
- Build the nav items and state selector into the Colorado theme's menu so Colorado→California
  linking is native.
- **Result:** true WordPress pages at `/california/...`, editable by staff, same origin.

### Option B — Static section behind a reverse proxy (if WP shouldn't own it)
- Host the generated `public/california/` and `public/careers/` as static files.
- At the web/CDN layer, route `drnatmed.com/california/*` (and the careers path) to the static
  bucket while everything else continues to hit WordPress.
- Keep assets at `/assets/*` (already root-relative) or namespace them.
- **This requires hosting/infra work (proxy or path rule).** A standalone app does **not**
  "automatically" appear inside WordPress — that routing must be configured by whoever manages
  hosting/DNS/CDN. We do not claim otherwise.

> Either way: **do not publish or modify production Colorado pages without explicit written
> deployment authorization.**

## 2. Booking integration

- Public website **must not** be the clinical intake. The site routes to an approved,
  BAA-covered scheduling/telehealth vendor where identity, California location, medical
  history, documents, and consent are collected.
- Current config uses `provider: "demo-adapter"`. The demo adapter **never confirms an
  appointment** and shows an explicit "nothing was booked / no payment taken" message.
- **Before LIVE MODE**, confirm with the chosen vendor:
  1. Signed **HIPAA Business Associate Agreement**.
  2. Privacy configuration (no PHI to analytics/ads; no session replay in intake/portal).
  3. It supports: mobile booking, time-zone-correct slots, visible pricing, confirmation
     messages, and useful error states.
  4. In-workflow confirmation of the patient's physical California location.
- Set `integrations.booking.provider`, `newPatientUrl`, `renewalUrl`, flip
  `launchStatus.mode` to `live` and `bookingEnabled` to `true`. The build gate
  (`booking_is_live()`) only enables real CTAs when **all** of these are real.

## 3. Public forms (notify / inquiry / recruitment)

- Collect **minimal** data: name, email, (inquiry) state + message, (recruitment)
  license info + availability. **Never** diagnoses, medical history, or ID documents.
- Set `integrations.forms.endpoint` to an approved handler (serverless function, or a vetted
  form provider with a DPA). The client posts only the minimal fields; validation + honeypot
  spam protection are built in. Consider adding server-side rate limiting + a CAPTCHA if spam
  is observed.
- **CV uploads stay disabled** (`cvUploadEnabled: false`) until secure storage + access
  controls exist. Do not enable file uploads on a public endpoint without that.

## 4. Analytics (see MEASUREMENT-PRIVACY.md)
- Disabled in preview. When enabled, use a privacy-respecting tool, exclude clinical
  intake/portal flows entirely, and never transmit PHI, form answers, documents, patient
  identifiers, or sensitive URL params. No advertising pixels. No session replay.

## 5. Entity / corporate-practice-of-medicine
- California's corporate-practice-of-medicine doctrine (Bus. & Prof. Code §2400) generally bars
  a non-licensed corporation from employing physicians. The administrative/marketing brand and
  the professional medical entity that delivers care are likely **distinct** (e.g., an MSO
  supporting a California professional medical corporation).
- Name the administrative business and the professional medical entity, and describe their
  relationship, **only after legal confirmation** (`entity.confirmed: true`). Until then the
  site uses accurate, non-committal language.

## 6. Build & deploy
```bash
python3 build.py            # render -> ./public
python3 build.py --serve    # local preview at :8080
```
- Output is plain static HTML/CSS/JS — no secrets, no third-party scripts.
- For Option A, treat `public/` as a reference for the theme templates.
- For Option B, deploy `public/california/`, `public/careers/`, `public/assets/`,
  `public/robots.txt`, and the sitemap. Remove the preview `robots.txt` Disallow in production.
