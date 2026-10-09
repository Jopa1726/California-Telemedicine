# Assumptions, missing facts & launch requirements

## A. Documented assumptions (made to keep building; confirm or correct)
1. **Brand spelling** stays "Doctors of Natural Medicine"; California service labeled
   "Doctors of Natural Medicine — California." (Per brief.)
2. **Preferred URL** is `drnatmed.com/california/` with careers at
   `/careers/california-physicians/`. (Per brief.)
3. **Telemedicine-only** in California (no CA street office); evaluations by
   **California-licensed** physicians. (Required by MBC telehealth guidance.)
4. **Launch mode is the safe default.** The site ships "coming soon" with notify +
   physician inquiry only; no payments, no clinical bookings.
5. **Colorado reputation is context, not California proof.** Colorado reviews/figures are shown
   labeled as Colorado.
6. **Founding year ~2016** used only to describe Colorado history (from the Colorado Springs page).
7. **No redirects needed** — the expansion only adds URLs.
8. **Build stack:** zero-dependency static site, because the build sandbox has no npm registry
   access and no WordPress. Ports to a WP child theme or static-behind-proxy (see INTEGRATION.md).

## B. Conflicting / unverified claims on the live Colorado site (do NOT auto-pick)
Reconcile these against real records before reuse anywhere:
- "4.9 stars / over 2,000 Google reviews" (home) — needs a dated source of truth.
- "over 9,000 evaluations per year" (home) — strong claim; verify internal data.
- Founding/tenure wording ("In 2016…") vs. any other implied dates — confirm the authoritative year.
- Superlatives ("premier," "best prices," "least expensive," "price match and beat") — not ported
  to California; do not reuse unsubstantiated price/#1 claims.
- "cannabis prescription" phrasing on the about page — a recommendation is **not** a prescription;
  corrected on all California copy.

## C. Missing business facts (blocking the fields they map to)
Each is an explicit `TODO_` in `site.config.json` and renders as a visible placeholder, never a guess.
| Fact | Config field | Public impact until provided |
|---|---|---|
| CA new-patient price | `pricing.newEvaluation` + `pricing.published` | Pricing shows "confirmed before launch" |
| CA renewal price | `pricing.renewal` | same |
| What the fee includes | `pricing.whatsIncluded` | TODO card on pricing |
| Not-approved / refund policy | `pricing.notApprovedPolicy`, `legal.policies.refund` | TODO card + legal placeholder |
| California-licensed physician(s) | `physicians.list`, `physicians.verified` | Shows "our standard," no bios |
| Booking/telehealth vendor + URLs + BAA | `integrations.booking.*` | Demo adapter; no real booking |
| Public form endpoint | `integrations.forms.endpoint` | Forms don't transmit (preview message) |
| Support email + hours (with TZ) | `contact.supportEmail`, `contact.supportHours` | TODO on contact |
| Entity structure (admin vs. professional medical corp) | `entity.*` | Non-committal entity language |
| Approved policies (privacy/terms/telehealth/cancellation) | `legal.policies.*` | Clearly-labeled placeholders |
| Medical reviewer + review date | `legal.medicalReviewer`, `legal.lastReviewed` | No "physician-reviewed" claim shown |

## D. Blocking before LIVE MODE (all must be true to flip `launchStatus.mode: "live"`)
1. At least one **California-licensed** MD/DO contracted and consenting to be listed, with a
   working license-verification link.
2. The **professional medical entity** and its relationship to the administrative brand are
   **legally confirmed** (corporate-practice-of-medicine compliant).
3. **Scheduling/telehealth vendor** selected with a signed **BAA**, privacy configuration
   verified, and the demo adapter replaced with real booking URLs.
4. **Pricing** approved and `pricing.published: true`.
5. **Policies** (privacy, terms, telehealth consent, cancellation, refund) approved and inserted.
6. **Patient workflow** approved: public inquiry vs. secure clinical intake boundary enforced;
   in-workflow California-location confirmation.
7. Medical content **actually reviewed** by a qualified clinician before any "reviewed" label.
8. **Explicit written deployment authorization** from the business.

The build's `booking_is_live()` gate enforces #3/#4 technically — real booking CTAs cannot
render while the provider is the demo adapter or booking URLs are still `TODO`.

## E. Compliance guardrails honored in copy (verified against primary sources)
- Approval depends on the physician's evaluation; **never guaranteed**. — [MBC cannabis guidance](https://www.mbc.ca.gov/Resources/Medical-Resources/cannabis.aspx)
- A recommendation is **not** a conventional prescription; MMIC is a **separate, voluntary,
  county-administered** card we don't issue. — [CDPH MMIC FAQs](https://www.cdph.ca.gov/Programs/CHSI/Pages/MMICP-FAQs.aspx)
- Evaluating a California patient requires a **current California license**, in person or via
  telehealth. — [MBC telehealth](https://www.mbc.ca.gov/Resources/Medical-Resources/telehealth.aspx)
- MMIC exempts qualifying medicinal purchases from **sales & use tax** (benefit tied to the
  MMIC, not the recommendation alone); excise tax still applies. — [CDTFA cannabis](https://cdtfa.ca.gov/industry/cannabis/getting-started.htm)
- Non-licensed corporation generally may **not employ physicians** (CPOM, Bus. & Prof. Code §2400). — [MBC board material](https://www.mbc.ca.gov/About/Meetings/Material/31205/brd-AgendaItem9r-20230824.pdf)
- No cures/universal relief promises; "natural" ≠ risk-free; balanced risk/interaction education included.
- No minors' pathway advertised (would require a reviewed clinical pathway).
- No fake CA address/map/listing; no mass city pages; no "best/#1/guaranteed."
