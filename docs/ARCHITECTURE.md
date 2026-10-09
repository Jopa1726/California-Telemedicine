# Brand & URL architecture

## Brand decision
- Keep the established spelling **"Doctors of Natural Medicine."**
- Position the new service as **"Doctors of Natural Medicine — California."**
- California is a **distinct service section inside the existing brand**, not a new brand,
  not a platform migration, and not a replacement of the Colorado site.

## URL map (preferred)
California lives under `/california/`. Colorado URLs are untouched.

| Path | Purpose | Canonical |
|---|---|---|
| `/california/` | California patient homepage (A–I sequence) | self |
| `/california/how-it-works/` | 3-step flow + pre-booking state router | self |
| `/california/pricing/` | Our fee vs. optional county MMIC fee | self |
| `/california/renewals/` | Renewal guidance | self |
| `/california/physicians/` | Physician standard + profiles (when verified) | self |
| `/california/faq/` | Full FAQ (all required questions) | self |
| `/california/resources/` | Rec vs. MMIC explainer, risks, sources | self |
| `/california/contact/` | Notify + public inquiry + support | self |
| `/california/legal/` | Privacy, terms, telehealth, cancellation, refund, accessibility, medical disclaimer | self |
| `/careers/california-physicians/` | Physician recruitment | self |

**Existing Colorado URLs preserved** (examples; do not change): `/`, `/colorado-springs/`,
`/medical-marijuana-doctor-denver/` (Lakewood), `/fort-colllins-clinic/`, `/pueblo/`,
`/locations/`, `/faq/`, `/appointment/`, `/apply-mmj-card-colorado/`,
`/medical-marijuana-card-renewal-colorado/`, etc.

## Cross-linking (both directions)
- **Colorado → California:** add a "California (telemedicine)" item to the Colorado primary
  nav and a state selector in the header. (In this preview the selector links CA↔CO.)
- **California → Colorado:** footer links to Colorado home and each clinic; the pre-booking
  router sends Colorado patients to `https://drnatmed.com/appointment/`.
- **State selector** is visible site-wide in the header on every California page.

## State-specific booking destinations
- California new patient → `integrations.booking.newPatientUrl` (TODO; demo adapter until set).
- California renewal → `integrations.booking.renewalUrl` (TODO).
- Colorado → existing `https://drnatmed.com/appointment/`.

## Canonicals
- Every distinct California page **self-references** its canonical (verified in build output).
- **Do NOT** canonicalize California service pages to Colorado pages. California pages are
  unique content and must stand on their own in search.

## Titles / descriptions / headings
- Unique, California-specific `<title>` and meta description per page (see `build.py` PAGE_MAP).
- One `<h1>` per page (QA-verified), descriptive H2/H3 structure.

## Structured data
- `MedicalBusiness` with `parentOrganization` → Doctors of Natural Medicine, `areaServed` =
  California, and an `availableService` of telemedicine cannabis evaluation.
- Based on **real** entities/services only. **No fake LocalBusiness with a California street
  address, no fake geo, no fake aggregateRating.** Add `aggregateRating`/`review` only when
  real, attributable California reviews exist; add `Physician` entries only for verified
  California-licensed physicians who consent.

## Sitemap & indexability
- `build.py` generates `/california/sitemap-california.xml` listing all California + careers
  pages with `lastmod`.
- On production, add these URLs to (or reference this file from) the existing WordPress
  sitemap/robots so Colorado and California are both discoverable.
- Preview `robots.txt` is deliberately conservative (it disallows `/california/legal/` which
  is placeholder-only and discourages indexing of non-production preview hosts). **On
  production, remove the Disallow and keep the Sitemap line.** All pages ship
  `<meta name="robots" content="index,follow">`.

## Redirects / migration map
- **None required for this expansion** — it only *adds* `/california/` and
  `/careers/california-physicians/`. No existing URL changes, so no redirects.
- If, later, any existing URL genuinely changes, add a 301 from old→new at that time.
  Do not create redirects speculatively.

## What we deliberately did NOT do
- No fake California office addresses, maps, or local listings (service is telemedicine-only).
- No hundreds of near-identical city pages. Start with strong statewide pages; city pages
  only when they add unique, accurate value (see SEO plan).
- No promise of ranking transfer, first-place rankings, or guaranteed traffic.
