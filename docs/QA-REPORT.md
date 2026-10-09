# QA report

**Build:** `python3 build.py` → 10 pages, LAUNCH MODE, booking live = False, pricing published = False.
**Preview:** `python3 -m http.server` (standard library).

## Tested & passing
| Check | Result |
|---|---|
| All 10 routes return 200 (served) | PASS — `/california/` + 7 subpages, `/careers/california-physicians/`, `/california/legal/` |
| CSS + JS + sitemap + robots return 200 | PASS |
| No unresolved `{{ }}` tokens or `{% %}` blocks in output | PASS |
| Exactly one `<h1>` per page | PASS (10/10) |
| All `<img>` have `alt` | PASS |
| `lang="en"` on every page | PASS |
| Balanced tag nesting (parser) | PASS |
| Canonicals absolute & self-referencing | PASS (e.g. `/california/faq/` → self) |
| Internal nav root-relative (works local + prod) | PASS |
| Structured data uses real parent org + CA service, no fake geo/rating | PASS |
| **Launch-mode safety gate** | PASS — booking stays off with demo-adapter and/or TODO URLs; only true when mode=live + bookingEnabled + real provider + real URL |
| Live-mode render (temp flip) shows booking CTAs + real prices | PASS, then reverted to launch |
| Demo booking adapter never confirms an appointment | PASS — shows explicit "nothing booked / no payment" alert |
| Public forms do not transmit in preview | PASS — show "NOT sent anywhere" message |
| Forms: required-field validation + inline errors + honeypot | PASS (client-side; add server-side before launch) |
| CV upload disabled on recruitment form | PASS |
| Reduced-motion respected (reveals + scroll) | PASS (CSS `prefers-reduced-motion` + JS check) |
| No third-party scripts / pixels / trackers | PASS (grep: only `/assets/js/app.js`) |
| Colorado links intact (home + 4 clinics + appointment) | PASS |
| State selector present site-wide | PASS |

## Journey verification
- **California patient** → header CTA + hero + router "I'm in California" → launch: routed to
  notify; live: routed to secure booking. PASS.
- **California renewal** → router "renewing" + Renewals page. PASS.
- **Colorado patient** → state selector + router "I'm in Colorado" → `drnatmed.com/appointment/`. PASS.
- **Has a question** → router + Contact (public inquiry, no medical data). PASS.
- **Physician** → nav "For physicians" + router + `/careers/california-physicians/` inquiry. PASS.
- **Mobile nav** → hamburger toggles `.is-open`, backdrop, Escape closes, `aria-expanded` updates. PASS (logic + CSS; see note).

## Not verified / needs real-environment testing
- **Core Web Vitals / Lighthouse** not measured here (no headless browser in sandbox). Expected
  strong (static HTML, one small CSS file, one small deferred JS, inline SVG, no web fonts/JS libs),
  but **measure on staging** before launch.
- **Real browser rendering & cross-device** (visual + mobile tap targets) not executed in-sandbox;
  review on a device lab / BrowserStack.
- **Screen-reader pass** (NVDA/VoiceOver) — structure is AA-oriented (skip link, landmarks, labeled
  fields, focus states, `aria-current`), but run a real AT pass before launch.
- **Form endpoint, booking vendor, analytics** — all TODO/demo; verify end-to-end once configured,
  including that failed submissions show useful errors against the live endpoint.
- **Sitemap/robots in production** — remove preview `Disallow`, wire into WP sitemap.
- **Spam protection** — honeypot only in preview; add server-side rate limiting/CAPTCHA.

## How to re-run
```bash
cd drnatmed-california
python3 build.py
python3 -m http.server 8080 --directory public   # http://localhost:8080/california/
```
