# SEO preservation + California content plan

## Part 1 — Preserve Colorado SEO
1. **Add, don't replace.** `/california/` is a new section; every Colorado URL stays live.
   No platform migration, no bulk URL changes, so **no redirects** are introduced.
2. **Keep the Colorado homepage** as the brand's primary entity. California is a child section
   with its own `MedicalBusiness` schema referencing the parent org.
3. **Self-canonical California pages.** Never canonicalize California pages to Colorado ones.
4. **Sitemaps.** Keep the existing Colorado sitemap; add the California sitemap
   (`/california/sitemap-california.xml`) so both are discoverable. Verify indexability
   (all pages are `index,follow`).
5. **Internal links both ways** (state selector + nav + footer) distribute authority to
   `/california/` while keeping Colorado navigation intact.
6. **No cannibalization.** California pages target California intent ("California medical
   cannabis recommendation"), distinct from Colorado "red card" intent, so they don't compete
   with Colorado rankings.
7. **Honest expectations.** Existing brand reputation can *support* trust, but California
   visibility still requires relevant content and ongoing work. **No** promise of automatic
   ranking transfer, first place, or guaranteed traffic.

## Part 2 — California content plan (statewide first)
Each piece ships with author info, a **genuine** reviewer attribution (only after real review),
source references, and accurate update dates. **No fabricated review dates or reviewers.**

| # | Working title | Primary intent | Status |
|---|---|---|---|
| 1 | How online medical cannabis evaluations work in California | informational | Built (How-it-works) |
| 2 | Recommendation vs. the county-issued MMIC | informational | Built (Resources + home §E) |
| 3 | What to prepare before your California appointment | informational | Built (Renewals/Resources) |
| 4 | California recommendation renewals: how they work | informational | Built (Renewals) |
| 5 | Understanding the real cost (our fee vs. county MMIC) | informational / commercial | Built (Pricing + Resources) |
| 6 | Medical vs. adult-use access in California | informational | Built (FAQ #12 + Resources) |
| 7 | Questions to ask a physician about cannabis | informational | Built (Resources) |
| 8 | Risks, side effects & medication interactions | informational / YMYL | Built (Resources) |

## Part 3 — Keyword hypotheses (validate before relying on them)
Treat these as **hypotheses**, not facts. Validate with real search data (Search Console,
a keyword tool) before optimizing hard. **No invented search-volume numbers.** Use terms
naturally; avoid stuffing.
- california medical marijuana evaluation
- california medical cannabis recommendation
- online medical marijuana doctor california
- california medical marijuana renewal
- california medical card vs recreational / MMIC
- do i need a medical card in california (and tax-savings angle)

## Part 4 — Local / city pages (disciplined)
- **Start with strong statewide pages.** Do **not** mass-produce near-identical city pages.
- Add a city page only when it offers **unique, accurate** value and correctly describes a
  **telemedicine** service available statewide (not a fake local office).

## Part 5 — Fast-follow opportunities
- **Spanish-language parity** for the core California pages (matches Leafwell's localization;
  `<html lang="es">`, hreflang pairing, translated + separately reviewed content).
- Structured FAQ (`FAQPage` schema) once copy is final and medically reviewed.
- Add verified `Physician` and (real) `review` structured data as those assets land.

## Measurement of SEO
- Track California service visits, booking starts/completions, contact + physician inquiries,
  conversion by device, and **search performance by state** (segment Search Console by the
  `/california/` path). See MEASUREMENT-PRIVACY.md for the privacy constraints.
