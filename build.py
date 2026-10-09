#!/usr/bin/env python3
"""
Doctors of Natural Medicine - California: zero-dependency static site renderer.

Standard library only (no pip installs needed). Renders templates/*.html page
bodies into a shared layout, injecting values from site.config.json, and writes
the result to public/california/ (plus /careers/ and legal pages).

Usage:
    python3 build.py            # build into ./public
    python3 build.py --serve    # build, then serve ./public on :8080

Design notes:
  * Pages are plain HTML fragments in templates/pages/. Shared chrome lives in
    templates/partials/ (head, header, footer).
  * {{ tokens }} are replaced from a flat context dict derived from the config.
  * {% if KEY %}...{% endif %} supports a single level of conditional blocks so a
    page can hide a section when a fact is unverified (e.g. pricing not published).
  * Launch mode is HARD-GATED here: when launchStatus.mode != 'live' OR
    bookingEnabled is false OR the booking provider is the demo-adapter, every
    booking CTA renders as a disabled "notify me" action and the demo booking
    page refuses to confirm an appointment. This cannot be bypassed from content.
"""
import json
import os
import re
import shutil
import sys
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "templates")
PAGES = os.path.join(TPL, "pages")
PARTIALS = os.path.join(TPL, "partials")
OUT = os.path.join(ROOT, "public")
CONFIG = os.path.join(ROOT, "site.config.json")

# Base path prefix for all internal/asset links. Empty for domain-root hosting
# (production drnatmed.com + local python http.server). Set to "/California-Telemedicine"
# for a GitHub Pages project site. No trailing slash.
BASE_PATH = os.environ.get("SITE_BASE_PATH", "").rstrip("/")

# ---- page registry: (template, output path, <title>, meta description, nav key) ----
PAGE_MAP = [
    ("home.html",            "california/index.html",                      "Medical Cannabis Evaluations in California by Telemedicine | Doctors of Natural Medicine", "California medical cannabis evaluations by telemedicine with a California-licensed physician, from an established clinic brand. See how it works, pricing, and FAQs.", "home"),
    ("how-it-works.html",    "california/how-it-works/index.html",         "How Online California Medical Cannabis Evaluations Work | DrNatMed California", "A clear, three-step look at how a California medical cannabis evaluation by telemedicine works, and what the physician decides.", "how"),
    ("pricing.html",         "california/pricing/index.html",              "California Medical Cannabis Evaluation Pricing | DrNatMed California", "Transparent pricing for California medical cannabis evaluations, plus how the optional county MMIC fee is separate from our fee.", "pricing"),
    ("renewals.html",        "california/renewals/index.html",             "California Medical Cannabis Recommendation Renewals | DrNatMed California", "How to renew your California medical cannabis recommendation by telemedicine, what to prepare, and how timing works.", "renewals"),
    ("physicians.html",      "california/physicians/index.html",           "Our California Physicians | DrNatMed California", "Meet the California-licensed physicians behind our telemedicine evaluations and how to verify their licenses.", "physicians"),
    ("faq.html",             "california/faq/index.html",                  "California Medical Cannabis Evaluation FAQ | DrNatMed California", "Answers to common questions about California medical cannabis evaluations, eligibility, cost, the MMIC, renewals, and privacy.", "faq"),
    ("resources.html",       "california/resources/index.html",            "California Medical Cannabis Patient Resources | DrNatMed California", "Plain-language guides to California medical cannabis access: recommendation vs. MMIC, costs, risks, and preparing for your appointment.", "resources"),
    ("contact.html",         "california/contact/index.html",              "Contact & Patient Support | DrNatMed California", "Get help or launch updates for the California telemedicine service. Public inquiries only — never send medical records by email.", "contact"),
    ("careers.html",         "careers/california-physicians/index.html",   "California-Licensed Physicians: Join Our Telemedicine Team | DrNatMed", "Bring thoughtful medical cannabis care to patients across California. Clinical autonomy, administrative support, and a careful telemedicine workflow.", "careers"),
    ("legal.html",           "california/legal/index.html",                "Privacy, Terms, Telehealth & Policies | DrNatMed California", "Privacy, terms, telehealth consent, cancellation, refund, and accessibility information for the California telemedicine service.", "legal"),
]


def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def booking_is_live(cfg):
    """Hard gate. ALL conditions must hold for real booking CTAs to render."""
    ls = cfg["launchStatus"]
    bk = cfg["integrations"]["booking"]
    return (
        ls.get("mode") == "live"
        and ls.get("bookingEnabled") is True
        and bk.get("provider") not in ("demo-adapter", None, "")
        and not str(bk.get("newPatientUrl", "")).startswith("TODO")
    )


def build_context(cfg):
    brand = cfg["brand"]
    live = booking_is_live(cfg)
    ls = cfg["launchStatus"]
    ctx = {
        "BRAND_CA": brand["californiaName"],
        "BRAND": brand["name"],
        "CO_HOME": brand["coloradoHome"],
        # BASE_PATH lets the same build work at the domain root (production:
        # drnatmed.com/california/) OR under a sub-path (GitHub Pages project site:
        # /California-Telemedicine/). Set via the SITE_BASE_PATH env var, no trailing slash.
        # Internal + asset links are root-relative so they work identically in local
        # preview and on the configured base. Canonicals/OG tags stay absolute.
        "CA_BASE": BASE_PATH + "/california/",
        "CAREERS": BASE_PATH + "/careers/california-physicians/",
        "ASSETS": BASE_PATH + "/assets",
        "BASE_PATH": BASE_PATH,
        "ORIGIN": brand["canonicalOrigin"],
        "CA_BASE_ABS": brand["californiaBase"],
        "CO_PHONE": brand["coloradoPhone"],
        "CO_PHONE_HREF": brand["coloradoPhoneHref"],
        "ESTABLISHED": brand["establishedYear"],
        "YEAR": str(date.today().year),
        "BUILD_DATE": date.today().isoformat(),
        "LAUNCH_MODE": ls["mode"],
        "LAUNCH_BANNER": ls["liveBanner"] if live else ls["launchBanner"],
        "CO_BOOKING_URL": cfg["integrations"]["booking"]["coloradoBookingUrl"],
        "CO_REVIEW_TEXT": cfg["reviews"]["coloradoAggregate"]["ratingText"],
        "CO_REVIEW_LABEL": cfg["reviews"]["coloradoAggregate"]["label"],
        "SUPPORT_EMAIL": cfg["contact"]["supportEmail"],
        "NOTIFY_CONSENT": cfg["contact"]["notifyConsentText"],
        "MMIC_FEE_NOTE": cfg["pricing"]["stateMmicFeeNote"],
        "ACCESS_TARGET": cfg["legal"]["policies"]["accessibilityTarget"],
    }
    # Flags for {% if %} blocks
    ctx["_FLAGS"] = {
        "BOOKING_LIVE": live,
        "PRICING_PUBLISHED": cfg["pricing"].get("published", False) and not str(cfg["pricing"].get("newEvaluation", "")).startswith("TODO"),
        "PHYSICIANS_VERIFIED": cfg["physicians"].get("verified", False),
        "CA_REVIEWS": cfg["reviews"]["californiaReviews"].get("show", False),
        "ANALYTICS": cfg["integrations"]["analytics"].get("enabled", False),
        "LAUNCH_MODE": not live,
    }
    # Pricing display strings (safe when not published)
    if ctx["_FLAGS"]["PRICING_PUBLISHED"]:
        ctx["PRICE_NEW"] = f"${cfg['pricing']['newEvaluation']}"
        ctx["PRICE_RENEWAL"] = f"${cfg['pricing']['renewal']}"
    else:
        ctx["PRICE_NEW"] = "confirmed before launch"
        ctx["PRICE_RENEWAL"] = "confirmed before launch"
    return ctx


def render_conditionals(text, flags):
    """Minimal {% if FLAG %}...{% else %}...{% endif %} (single level)."""
    pattern = re.compile(r"\{%\s*if\s+(\w+)\s*%\}(.*?)(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}", re.S)

    def repl(m):
        flag, truthy, falsy = m.group(1), m.group(2), m.group(3) or ""
        return truthy if flags.get(flag) else falsy

    # loop to resolve nested-after-expansion cases
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub(repl, text)
    return text


def render_tokens(text, ctx):
    def repl(m):
        key = m.group(1)
        return str(ctx.get(key, m.group(0)))
    pat = re.compile(r"\{\{\s*(\w+)\s*\}\}")
    # loop so tokens injected by other tokens (e.g. NAV containing CA_BASE) resolve
    prev = None
    passes = 0
    while prev != text and passes < 6:
        prev = text
        text = pat.sub(repl, text)
        passes += 1
    return text


def nav_html(active):
    items = [
        ("home", "Overview", "{{CA_BASE}}"),
        ("how", "How it works", "{{CA_BASE}}how-it-works/"),
        ("pricing", "Pricing", "{{CA_BASE}}pricing/"),
        ("renewals", "Renewals", "{{CA_BASE}}renewals/"),
        ("physicians", "Physicians", "{{CA_BASE}}physicians/"),
        ("faq", "FAQ", "{{CA_BASE}}faq/"),
        ("resources", "Resources", "{{CA_BASE}}resources/"),
        ("contact", "Contact", "{{CA_BASE}}contact/"),
    ]
    lis = []
    for key, label, href in items:
        cur = ' aria-current="page"' if key == active else ""
        lis.append(f'<li><a href="{href}"{cur}>{escape(label)}</a></li>')
    return "\n".join(lis)


def build():
    cfg = load_config()
    ctx = build_context(cfg)
    flags = ctx.pop("_FLAGS")

    head = read(os.path.join(PARTIALS, "head.html"))
    header = read(os.path.join(PARTIALS, "header.html"))
    footer = read(os.path.join(PARTIALS, "footer.html"))
    layout = read(os.path.join(PARTIALS, "layout.html"))

    # clean output
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # copy static assets
    shutil.copytree(os.path.join(TPL, "assets"), os.path.join(OUT, "assets"))

    sitemap_urls = []
    for tpl_name, out_rel, title, desc, nav_key in PAGE_MAP:
        body = read(os.path.join(PAGES, tpl_name))
        canonical = ctx["CA_BASE"].rstrip("/") + "/"
        # canonical from output path
        url_path = "/" + out_rel.replace("index.html", "")
        canonical = ctx["ORIGIN"] + url_path
        page_ctx = dict(ctx)
        page_ctx.update({
            "TITLE": title,
            "DESC": desc,
            "CANONICAL": canonical,
            "NAV": nav_html(nav_key),
            "ACTIVE": nav_key,
        })
        # assemble: layout holds {{HEAD}} {{HEADER}} {{BODY}} {{FOOTER}}
        page = layout
        page = page.replace("{{HEAD}}", head)
        page = page.replace("{{HEADER}}", header)
        page = page.replace("{{BODY}}", body)
        page = page.replace("{{FOOTER}}", footer)
        # conditionals first, then tokens
        page = render_conditionals(page, flags)
        page = render_tokens(page, page_ctx)

        out_path = os.path.join(OUT, out_rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        sitemap_urls.append((canonical, tpl_name))

    write_sitemap(ctx, sitemap_urls)
    write_robots(ctx)
    # .nojekyll so GitHub Pages serves files as-is (no Jekyll processing)
    with open(os.path.join(OUT, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")
    # Root index: redirects the bare base URL to /california/ (handy for GitHub Pages
    # project sites where the repo root has no landing page).
    root_redirect = read(os.path.join(PAGES, "_root-redirect.html"))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_redirect)
    print(f"Built {len(PAGE_MAP)} pages -> {OUT}")
    print(f"Launch mode: {ctx['LAUNCH_MODE']}  |  Booking live: {flags['BOOKING_LIVE']}  |  Pricing published: {flags['PRICING_PUBLISHED']}")
    if not flags["BOOKING_LIVE"]:
        print("NOTE: LAUNCH MODE active — booking CTAs render as 'notify me'; no appointment can be confirmed.")


def write_sitemap(ctx, urls):
    today = ctx["BUILD_DATE"]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for canonical, _ in urls:
        lines.append(f"  <url><loc>{canonical}</loc><lastmod>{today}</lastmod></url>")
    lines.append("</urlset>")
    with open(os.path.join(OUT, "california", "sitemap-california.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_robots(ctx):
    # Preview-safe robots: in LAUNCH preview we discourage indexing of the preview host.
    txt = (
        "# Preview robots.txt. On production, REMOVE Disallow and keep the sitemap line.\n"
        "User-agent: *\n"
        "Disallow: /california/legal/\n"
        f"Sitemap: {ctx['ORIGIN']}/california/sitemap-california.xml\n"
    )
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def serve():
    import http.server
    import socketserver
    os.chdir(OUT)
    port = 8080
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving {OUT} at http://localhost:{port}/california/")
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
