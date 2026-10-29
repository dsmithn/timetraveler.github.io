#!/usr/bin/env python3
"""Check the site's pages against site-facts.md before any push.

Run by Destin before any push, never by Devin:
    python3 check-facts.py                    # exit 1 on any drift
    python3 check-facts.py --update-locations # rewrite the "Where each fact appears" table

Fails on: a phone number, email, license, price, discount, visit count, hours,
founding year or service-area value (visible text or JSON-LD) that differs from
site-facts.md or is attached to the wrong plan or day; any BBB mention or bbb.org link
(the business is not accredited); an age claim like "12+ years"; JSON-LD that differs
between pages; a plan card whose full text is not the approved card (CARD_TEMPLATES;
change its season wording there); price, discount or billing-basis text outside a plan card that is not one of PRICED_TEXTS; a holiday
notice without both dates; a sample photo (assets/placeholders/) without its visible "Sample photo,
replace with yours" tag or its row under "Photos Devin needs to provide", or a row with no sample on
any page; any texting mention while SMS_ENABLED is false; an internal link
or asset that doesn't exist; a root-absolute or trailing-slash internal URL; a
stale locations table.

Limits: it checks fact values where they appear. A brand-new sentence that
makes a new claim (a new city, "open 24/7", "ten percent off") is not a
fact drift it can see; copy changes still get read before a push.
"""
from __future__ import annotations

import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACTS_FILE = ROOT / "site-facts.md"
PAGES = ["index.html", "maintenance.html", "register.html"]
PLAN_PAGES = ["index.html", "maintenance.html"]
PLANS = {"Annual": "ANNUAL", "Semi-annual": "SEMI", "Quarterly": "QUARTERLY"}
LOC_START, LOC_END = "<!-- LOCATIONS:START -->", "<!-- LOCATIONS:END -->"
PHOTOS_START, PHOTOS_END = "<!-- PHOTOS:START -->", "<!-- PHOTOS:END -->"
PH_DIR = "assets/placeholders/"
PH_TAG = "Sample photo, replace with yours"
PH_FILE_RE = re.compile(r"assets/placeholders/([a-z0-9-]+)-\d+\.webp")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HIDE_RE = re.compile(r"display:none|visibility:hidden|opacity:0(?:\.0*)?(?:;|$|!)")


def hides(a: dict[str, str]) -> bool:
    """True when an element's own attributes hide it."""
    return any(k in a for k in ("hidden", "aria-hidden", "inert")) or bool(HIDE_RE.search(re.sub(r"\s", "", a.get("style", "").lower())))


def ph_path(url: str) -> str | None:
    """The url as a site path when it points into assets/placeholders/ (any spelling), else None."""
    path = posixpath.normpath(re.sub(r"^(?:https?:)?//[^/]+", "", url.split("#")[0].split("?")[0].strip()).lstrip("/"))
    return path if "assets/placeholders/" in path + "/" else None

PHONE_RE = re.compile(r"(?<![\w$])(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)")
RUN_PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
LICENSE_RE = re.compile(r"\b[A-Z]{2,3}\d{6,7}\b")
PRICE_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")
PERCENT_RE = re.compile(r"\d+(?:\.\d+)?\s?%")
VISITS_RE = re.compile(r"(\d+) visits? (?:a|per|each|every) (\w+)")
TIME = r"\d{1,2}(?::\d\d)?\s?(?:[AaPp][Mm]|[AaPp]\.[Mm]\.)"
RANGE_RE = re.compile(rf"({TIME})\s*(?:[–—-]|to)\s*({TIME})")
TEXTING_RE = re.compile(r"\b(sms|texts?|texting|texted)\b", re.I)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
# A year is checked only in text that talks about the business's age, so a holiday notice or a copyright line passes.
FOUNDING_WORDS = re.compile(r"\b(?:since|incorporated|founded|established|est\.|started|opened|serving|in business)(?=\W)", re.I)
# "12+ years", "over 10 years", "10 years in business", "a decade": the founding line is the only tenure claim.
AGE_CLAIM_RE = re.compile(r"\b\d+\s?\+\s?years?\b|\b(?:over|more than|nearly|almost|about)\s+\d+\s+years?\b|"
                          r"\b\d+\s+years?\s+(?:in business|of experience|of service|experience|serving)\b|\bdecades?\b", re.I)
BBB_RE = re.compile(r"\bBBB\b|Better Business Bureau", re.I)  # not accredited, so the site carries no rating
# Places outside the stated service area. areaServed must match AREA_LINE, so naming these is drift.
OTHER_PLACES = re.compile(r"\b(broward|miami|fort lauderdale|ft\.? lauderdale|hollywood|coral springs|margate|coconut creek|"
                          r"lighthouse point|hillsboro beach|parkland|tamarac|sunrise|plantation|martin county|stuart|"
                          r"st\.? lucie|port st|hobe sound)\b", re.I)
# Any text that names part of the service area must be one of these complete texts, so an appended
# place ("... and Orlando") fails. {KEY} is a fact value.
AREA_WORDS = re.compile(r"palm beach|deerfield|pompano|county|counties", re.I)
AREA_TEXTS = [
    "{AREA_LINE}",
    "Family-owned AC repair in Delray Beach. {AREA_LINE}",
    "Family-owned AC repair, installation and maintenance in Delray Beach and all of Palm Beach County. {SERVICE_CALL} service call. Call {PHONE_DISPLAY}.",
    "Family-owned AC repair, installation and maintenance in Delray Beach and all of Palm Beach County. Call {PHONE_DISPLAY}.",
    "AC maintenance plans in Palm Beach County: {PLAN_ANNUAL}, {PLAN_SEMI} or {PLAN_QUARTERLY} a year for one system, with a 14-point check on every visit. Call {PHONE_DISPLAY}.",
]
# The only sentences outside a plan card that may carry a price or a discount. {KEY} is a fact value.
LOOSE_TEMPLATES = [
    "{SERVICE_CALL} service call",
    "{SERVICE_CALL}. That covers the visit",
    "The regular service call is {SERVICE_CALL}",
    "starting at {PLAN_ANNUAL} a year",
    "Plans from {PLAN_ANNUAL} a Year",
    "{PLAN_ANNUAL}, {PLAN_SEMI} or {PLAN_QUARTERLY} a year",
    "members get {PLAN_ANNUAL_DISCOUNT} off, or {PLAN_QUARTERLY_DISCOUNT} on the quarterly plan",
]
# Outside plan cards, any block of text that carries a price, a discount or a billing basis must be one
# of these complete texts, so "per hour" after "$99 service call" or "per month for two systems" fails.
BASIS_RE = re.compile(r"\bprices are\b|\bper (?:year|month|week|day|visit|hour|trip)\b|\b(?:monthly|weekly|hourly)\b|"
                      r"\ban? (?:month|week|hour)\b", re.I)
PRICED_TEXTS = [
    "Family-owned AC repair, installation and maintenance in Delray Beach and all of Palm Beach County. {SERVICE_CALL} service call. Call {PHONE_DISPLAY}.",
    "{SERVICE_CALL} service call to diagnose (repairs quoted before work)",
    "One, two or four visits a year, starting at {PLAN_ANNUAL} a year for one system.",
    "Prices are per year for one system. Every visit covers the same 14-point check.",
    "{SERVICE_CALL}. That covers the visit and finding the problem. We tell you what the repair costs before we do it. "
    "Maintenance plan members get {PLAN_ANNUAL_DISCOUNT} off, or {PLAN_QUARTERLY_DISCOUNT} on the quarterly plan.",
    "AC Maintenance Plans from {PLAN_ANNUAL} a Year | Major Tom's Air Repair",
    "AC maintenance plans in Palm Beach County: {PLAN_ANNUAL}, {PLAN_SEMI} or {PLAN_QUARTERLY} a year for one system, with a 14-point check on every visit. Call {PHONE_DISPLAY}.",
    "Pick how often you want us out. Prices are per year and cover one system.",
    "The regular service call is {SERVICE_CALL}. That covers the visit and finding the problem, and we quote any repair before we start it. "
    "Plan discounts come off that price and off the repair.",
]
# Tags that do not break a run of text, so "(561) 860-<strong>3671</strong>" is read as one number.
INLINE = {"a", "abbr", "b", "code", "em", "i", "mark", "s", "small", "span", "strong", "sub", "sup", "time", "u"}
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


class Page(HTMLParser):
    """Collects visible text (with line numbers), plan cards, link targets, ids and JSON-LD."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[tuple[int, str, bool]] = []
        self.runs: list[tuple[int, str, bool]] = []  # visible text joined across inline tags
        self.attrs: list[tuple[int, str]] = []
        self.holiday: dict[str, str] = {}
        self.plans: list[tuple[int, str, list[str]]] = []
        self.links: list[tuple[int, str, str]] = []
        self.ids: set[str] = set()
        self.jsonld: list[str] = []
        self.figures: list[dict] = []  # {"line", "ph", "hidden", "imgs": [(line, path)], "tags": [{"text", "hidden", "markup"}]}
        self.loose_ph: list[tuple[int, str]] = []  # sample photos outside any <figure>
        self.photo_problems: list[tuple[int, str]] = []  # nested or unclosed figures
        self._open: list[tuple[str, bool]] = []  # open elements and whether each hides itself
        self._figs: list[dict] = []
        self._tag: dict | None = None
        self._skip: str | None = None
        self._plan_depth = 0
        self._plan: list[str] = []
        self._run: list[str] = []
        self._run_at = (0, False)

    def _flush(self) -> None:
        text = " ".join("".join(self._run).split())
        if text:
            self.runs.append((self._run_at[0], text, self._run_at[1]))
        self._run = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        line = self.getpos()[0]
        if tag not in INLINE:
            self._flush()
        if "data-holiday-notice" in a:
            self.holiday = {k: a.get(f"data-holiday-{k}", "") for k in ("notice", "from", "until")} | {"line": str(line)}
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "li" and self._plan_depth:
            self._plan_depth += 1
        elif tag == "li" and "plan" in a.get("class", "").split():
            self._plan_depth, self._plan = 1, [str(line)]
        classes = a.get("class", "").split()
        hidden = hides(a) or any(h for _, h in self._open)
        if self._tag is not None:
            self._tag["markup"] = True  # the label must be plain text
        if tag == "figure":
            if self._figs:
                self.photo_problems.append((line, "a <figure> starts inside another <figure>; close the first one"))
            self._figs.append({"line": line, "ph": "ph" in classes, "hidden": hidden, "imgs": [], "tags": [], "at": len(self._open)})
        if tag in ("img", "source"):
            urls = [a.get("src", "")] + [s.split()[0] for s in a.get("srcset", "").split(",") if s.strip()]
            found = [(line, path) for path in map(ph_path, urls) if path]
            (self._figs[-1]["imgs"] if self._figs else self.loose_ph).extend(found)
        if tag == "span" and "ph-tag" in classes:
            self._tag = {"text": "", "hidden": hidden, "markup": False, "at": len(self._open)}
            if self._figs:
                self._figs[-1]["tags"].append(self._tag)
        if tag not in VOID:
            self._open.append((tag, hides(a)))
        if tag == "script":
            self._skip = "jsonld" if a.get("type") == "application/ld+json" else "script"
        elif tag == "style":
            self._skip = "style"
        for attr in ("href", "src", "action", "data-mailto"):
            if attr in a:
                self.links.append((line, attr, a[attr]))
        for attr in ("srcset", "imagesrcset"):
            for part in a.get(attr, "").split(","):
                if part.strip():
                    self.links.append((line, attr, part.split()[0]))
        for attr in ("aria-label", "alt", "title", "placeholder", "data-holiday-notice", "data-closed-suffix", "content"):
            if a.get(attr):
                self.text.append((line, a[attr], False))
                self.attrs.append((line, a[attr]))

    def handle_endtag(self, tag: str) -> None:
        if tag not in INLINE:
            self._flush()
        if tag in ("script", "style"):
            self._skip = None
        names = [n for n, _ in self._open]
        if tag in names:
            del self._open[len(names) - 1 - names[::-1].index(tag):]
        if self._tag is not None and len(self._open) <= self._tag["at"]:
            self._tag = None
        while self._figs and len(self._open) <= self._figs[-1]["at"]:
            self.figures.append(self._figs.pop())
        if tag == "li" and self._plan_depth:
            self._plan_depth -= 1
            if not self._plan_depth:
                nodes = [" ".join(d.split()) for d in self._plan[1:]]
                self.plans.append((int(self._plan[0]), " ".join(" ".join(nodes).split()), nodes))

    def close(self) -> None:
        super().close()
        for fig in self._figs:
            self.photo_problems.append((fig["line"], "<figure> is never closed"))
            self.figures.append(fig)
        self._figs = []

    def handle_data(self, data: str) -> None:
        if self._tag is not None:
            self._tag["text"] += data
        if self._skip == "jsonld":
            self.jsonld.append(data)
        elif self._skip is None and data.strip():
            self.text.append((self.getpos()[0], data, bool(self._plan_depth)))
            if not self._run:
                self._run_at = (self.getpos()[0], bool(self._plan_depth))
            self._run.append(data)
            if self._plan_depth:
                self._plan.append(data)


def load_facts() -> dict[str, str]:
    block = re.search(r"```facts\n(.*?)```", FACTS_FILE.read_text(), re.S)
    if not block:
        sys.exit("site-facts.md has no ```facts block")
    facts = {}
    for raw in block.group(1).splitlines():
        if ":" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split(":", 1)
            facts[key.strip()] = value.strip()
    return facts


def to24(t: str) -> str:
    m = re.fullmatch(r"(\d{1,2})(?::(\d\d))? ([AP]M)", t)
    if not m:
        raise ValueError(f"bad time {t!r}")
    h = int(m.group(1)) % 12 + (12 if m.group(3) == "PM" else 0)
    return f"{h:02d}:{m.group(2) or '00'}"


def expected_hours(facts: dict[str, str]) -> list[dict[str, object]]:
    out = []
    for key, days in (("HOURS_WEEKDAYS", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]), ("HOURS_SATURDAY", "Saturday")):
        m = RANGE_RE.search(facts[key])
        out.append({"dayOfWeek": days, "opens": to24(m.group(1)), "closes": to24(m.group(2))})
    return out


def plan_offer_text(facts: dict[str, str], plan: str) -> str:
    visits = facts[f"PLAN_{plan}_VISITS"]
    return (f"Per year, one system: {visits} visit{'' if visits == '1' else 's'} a year. "
            f"Each extra system {facts[f'PLAN_{plan}_EXTRA_SYSTEM']}. {facts[f'PLAN_{plan}_DISCOUNT']} off service calls and repairs.")


def plan_clauses(facts: dict[str, str], plan: str) -> set[str]:
    """The only price- or discount-bearing clauses a plan card may contain, so a changed billing basis fails."""
    price, extra, off = facts[f"PLAN_{plan}"], facts[f"PLAN_{plan}_EXTRA_SYSTEM"], facts[f"PLAN_{plan}_DISCOUNT"]
    return {f"{price} a year", f"Each extra system: {extra}", f"Each extra system {extra}",
            f"{off} off service calls", f"{off} off repairs", f"{off} off service calls and repairs"}


# The complete text of each plan card, per page, so any added qualifier ("per visit", "first year
# only") fails wherever it sits in the card. Season wording is copy, not a fact. {KEY} is a fact value.
CARD_SEASONS = {
    "index.html": {"ANNUAL": " (fall or spring)", "SEMI": " (fall and spring)", "QUARTERLY": ""},
    "maintenance.html": {"ANNUAL": ", in the fall or spring", "SEMI": ", fall and spring", "QUARTERLY": ""},
}
CARD_TEMPLATES = {
    "index.html": "{name} {price} a year {visits} a year{season}. Each extra system {extra}. {off} off service calls and repairs.",
    "maintenance.html": "{name} {price} a year {visits} a year{season} Each extra system: {extra} {off} off service calls {off} off repairs",
}


def plan_card_text(facts: dict[str, str], page: str, name: str, plan: str) -> str:
    visits = facts[f"PLAN_{plan}_VISITS"]
    return CARD_TEMPLATES[page].format(
        name=name, price=facts[f"PLAN_{plan}"], visits=f"{visits} visit{'' if visits == '1' else 's'}",
        season=CARD_SEASONS[page][plan], extra=facts[f"PLAN_{plan}_EXTRA_SYSTEM"], off=facts[f"PLAN_{plan}_DISCOUNT"])


def uncovered(text: str, pattern: re.Pattern[str], allowed: list[str]) -> list[str]:
    """Matches of pattern in text that do not sit inside one of the allowed exact phrases."""
    spans = [(m.start(), m.start() + len(p)) for p in allowed if p for m in re.finditer(re.escape(p), text)]
    return [m.group(0) for m in pattern.finditer(text) if not any(s <= m.start() and m.end() <= e for s, e in spans)]


def check(facts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    sms_on = facts["SMS_ENABLED"].lower() == "true"
    tel = facts["PHONE_TEL"]
    jsonld_tel = f"+1-{tel[2:5]}-{tel[5:8]}-{tel[8:]}"
    area = [a.strip() for a in facts["AREA_JSONLD"].split(";")]
    loose = [t.format(**facts) for t in LOOSE_TEMPLATES]
    hours = [facts["HOURS_WEEKDAYS"], facts["HOURS_SATURDAY"]]
    founded = f"Incorporated {facts['INCORPORATED']}, licensed for installs and full-service work since {facts['LICENSED_SINCE']}"
    area_texts = {t.format(**facts) for t in AREA_TEXTS}
    priced_texts = {t.format(**facts) for t in PRICED_TEXTS}
    parsed: dict[str, Page] = {}
    first_ld = None

    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            errors.append(f"{name}: missing")
            continue
        page = Page()
        page.feed(path.read_text())
        page.close()
        page._flush()
        parsed[name] = page
        visible = " ".join(t for _, t, _ in page.text)

        for line, t, in_plan in page.text:
            where = f"{name}:{line}"
            for m in PHONE_RE.findall(t):
                if m != facts["PHONE_DISPLAY"]:
                    errors.append(f"{where}: phone {m!r} != {facts['PHONE_DISPLAY']!r}")
            for m in EMAIL_RE.findall(t):
                if m != facts["EMAIL"]:
                    errors.append(f"{where}: email {m!r} != {facts['EMAIL']!r}")
            for m in LICENSE_RE.findall(t):
                if m != facts["LICENSE"]:
                    errors.append(f"{where}: license {m!r} != {facts['LICENSE']!r}")
            if not in_plan:
                for m in uncovered(t, PRICE_RE, loose) + uncovered(t, PERCENT_RE, loose):
                    errors.append(f"{where}: {m} outside a plan card and not in a known sentence: {t.strip()[:70]!r}")
            for m in uncovered(t, RANGE_RE, hours):
                errors.append(f"{where}: hours {m!r} are not attached to their day as in site-facts.md")
            if BBB_RE.search(t):
                errors.append(f"{where}: mentions the BBB; the business is not accredited, so the site carries no rating: {t.strip()[:60]!r}")
            for m in uncovered(t, YEAR_RE, [founded]) if FOUNDING_WORDS.search(t) else []:
                errors.append(f"{where}: year {m!r} is not in the founding line from site-facts.md: {t.strip()[:60]!r}")
            if AGE_CLAIM_RE.search(t):
                errors.append(f"{where}: age claim {AGE_CLAIM_RE.search(t).group(0)!r}; the footer founding line is the only years claim")
            if AREA_WORDS.search(t) and " ".join(t.split()) not in area_texts:
                errors.append(f"{where}: service-area text is not one of the known sentences: {t.strip()[:80]!r}")
            if OTHER_PLACES.search(t):
                errors.append(f"{where}: names {OTHER_PLACES.search(t).group(0)!r}, outside {facts['AREA_LINE']!r}")
            if not sms_on and TEXTING_RE.search(t):
                errors.append(f"{where}: mentions texting while SMS_ENABLED is false: {t.strip()[:60]!r}")

        for line, t, in_plan in page.runs:
            where = f"{name}:{line}"
            for m in RUN_PHONE_RE.findall(t):  # by digits: "Call<span>(561)..." joins to "Call(561)..."
                if re.sub(r"\D", "", m)[-10:] != re.sub(r"\D", "", facts["PHONE_DISPLAY"]):
                    errors.append(f"{where}: phone {m!r} != {facts['PHONE_DISPLAY']!r} (text joined across inline tags)")
            for m in EMAIL_RE.findall(t) + LICENSE_RE.findall(t):
                if m not in (facts["EMAIL"], facts["LICENSE"]):
                    errors.append(f"{where}: {m!r} is not the site-facts.md email or license (text joined across inline tags)")
        for line, t in [(line, t) for line, t, in_plan in page.runs if not in_plan] + page.attrs:
            t = " ".join(t.split())
            if (PRICE_RE.search(t) or PERCENT_RE.search(t) or BASIS_RE.search(t)) and t not in priced_texts:
                errors.append(f"{name}:{line}: price, discount or billing text is not one of the known texts (PRICED_TEXTS): {t[:80]!r}")

        if page.holiday.get("notice"):
            h, where = page.holiday, f"{name}:{page.holiday['line']}"
            if not (DATE_RE.fullmatch(h["from"]) and DATE_RE.fullmatch(h["until"]) and h["from"] <= h["until"]):
                errors.append(f"{where}: a holiday notice needs data-holiday-from and data-holiday-until (YYYY-MM-DD, from <= until), "
                              f"got from={h['from']!r} until={h['until']!r}")

        for line, block, nodes in page.plans:
            where = f"{name}:{line}"
            plan = PLANS.get(block.split(" ")[0])
            if not plan:
                errors.append(f"{where}: plan card {block[:30]!r} is not Annual, Semi-annual or Quarterly")
                continue
            want_money = {facts[f"PLAN_{plan}"], facts[f"PLAN_{plan}_EXTRA_SYSTEM"]}
            if set(PRICE_RE.findall(block)) != want_money or f"{facts[f'PLAN_{plan}']} a year" not in block:
                errors.append(f"{where}: {plan.lower()} card prices {PRICE_RE.findall(block)} != {sorted(want_money)}")
            if set(PERCENT_RE.findall(block)) != {facts[f"PLAN_{plan}_DISCOUNT"]}:
                errors.append(f"{where}: {plan.lower()} card discounts {PERCENT_RE.findall(block)} != {facts[f'PLAN_{plan}_DISCOUNT']}")
            if name in CARD_TEMPLATES and block != (card := plan_card_text(facts, name, block.split(" ")[0], plan)):
                errors.append(f"{where}: {plan.lower()} card reads {block!r}, expected {card!r}")
            terms = plan_clauses(facts, plan)
            for clause in (c for n in nodes for c in re.split(r"(?<=\.)\s+", n)):
                if (PRICE_RE.search(clause) or PERCENT_RE.search(clause)) and clause.rstrip(".") not in terms:
                    errors.append(f"{where}: {plan.lower()} card clause {clause!r} is not one of {sorted(terms)}")
            if set(VISITS_RE.findall(block)) != {(facts[f"PLAN_{plan}_VISITS"], "year")} or re.search(r"month|week|quarter\b", block, re.I):
                errors.append(f"{where}: {plan.lower()} card visits {VISITS_RE.findall(block)} != {facts[f'PLAN_{plan}_VISITS']} a year")
        if name in PLAN_PAGES and sorted(PLANS.get(b.split(' ')[0], '?') for _, b, _ in page.plans) != sorted(PLANS.values()):
            errors.append(f"{name}: expected one Annual, one Semi-annual and one Quarterly plan card")

        for key in ("LICENSE", "HOURS_WEEKDAYS", "HOURS_SATURDAY", "HOURS_SUNDAY", "PHONE_DISPLAY"):
            if facts[key] not in visible:
                errors.append(f"{name}: does not show {key} {facts[key]!r}")
        if founded not in visible:
            errors.append(f"{name}: does not show {founded!r}")
        if name == "index.html" and visible.count(facts["AREA_LINE"]) < 2:
            errors.append("index.html: AREA_LINE should appear in the hero and the FAQ")

        for line, attr, url in page.links:
            where = f"{name}:{line}"
            low = url.lower()
            if "bbb.org" in low:
                errors.append(f"{where}: links to bbb.org; the business is not BBB accredited")
            if low.startswith("tel:") and url != f"tel:{tel}":
                errors.append(f"{where}: {url} != tel:{tel}")
            if low.startswith("sms:") and (not sms_on or url != f"sms:{tel}"):
                errors.append(f"{where}: {url} (SMS_ENABLED={facts['SMS_ENABLED']})")
            if low.startswith("mailto:") and url.split("?")[0] != f"mailto:{facts['EMAIL']}":
                errors.append(f"{where}: {url} != mailto:{facts['EMAIL']}")
            if attr == "action" and re.match(r"^(mailto:|http:)", low):
                errors.append(f"{where}: form action {url!r} is not HTTPS; browsers flag the form as insecure (Lighthouse is-on-https)")
            if re.match(r"^(https?:|mailto:|tel:|sms:|data:)", low):
                continue
            target, _, frag = url.partition("#")
            if url.startswith("/"):
                errors.append(f"{where}: root-absolute internal URL {url!r} breaks the preview; use a relative path")
            elif target.endswith("/") and target != "./":
                errors.append(f"{where}: trailing-slash internal URL {url!r}")
            file = name if target == "" else "index.html" if target == "./" else target
            if not (ROOT / file).is_file():
                errors.append(f"{where}: {attr} points to missing file {url!r}")
            elif frag and file.endswith(".html"):
                other = parsed.get(file)
                if other is None:
                    other = Page()
                    other.feed((ROOT / file).read_text())
                if frag not in other.ids:
                    errors.append(f"{where}: {url!r} has no #{frag} target")

        if len(page.jsonld) != 1:
            errors.append(f"{name}: expected one JSON-LD block, found {len(page.jsonld)}")
            continue
        try:
            ld = json.loads(page.jsonld[0])
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: JSON-LD does not parse: {exc}")
            continue
        if first_ld is None:
            first_ld = ld
        elif ld != first_ld:
            errors.append(f"{name}: JSON-LD differs from {PAGES[0]}")
        if ld.get("telephone") != jsonld_tel:
            errors.append(f"{name}: JSON-LD telephone {ld.get('telephone')!r} != {jsonld_tel!r}")
        if ld.get("email") != facts["EMAIL"]:
            errors.append(f"{name}: JSON-LD email {ld.get('email')!r}")
        ident = ld.get("identifier")
        if not isinstance(ident, dict) or ident.get("value") != facts["LICENSE"]:
            errors.append(f"{name}: JSON-LD license {ld.get('identifier')!r}")
        if [a.get("name") for a in ld.get("areaServed", [])] != area:
            errors.append(f"{name}: JSON-LD areaServed != AREA_JSONLD {area}")
        if "aggregateRating" in json.dumps(ld) or "streetAddress" in json.dumps(ld):
            errors.append(f"{name}: JSON-LD must not carry aggregateRating or a street address")
        if ld.get("foundingDate") != facts["INCORPORATED"]:
            errors.append(f"{name}: JSON-LD foundingDate {ld.get('foundingDate')!r} != INCORPORATED {facts['INCORPORATED']!r}")
        if "bbb.org" in json.dumps(ld).lower():
            errors.append(f"{name}: JSON-LD links to bbb.org; the business is not BBB accredited")
        got = [{k: s.get(k) for k in ("dayOfWeek", "opens", "closes")} for s in ld.get("openingHoursSpecification", [])]
        if got != expected_hours(facts):
            errors.append(f"{name}: JSON-LD hours {got} != site-facts.md {expected_hours(facts)}")
        want_offers = {"Service call": (facts["SERVICE_CALL"], "Visit to find the problem. Repairs are quoted before work starts.")}
        for plan, label in (("ANNUAL", "Annual"), ("SEMI", "Semi-annual"), ("QUARTERLY", "Quarterly")):
            want_offers[f"{label} maintenance plan"] = (facts[f"PLAN_{plan}"], plan_offer_text(facts, plan))
        got_offers = {o.get("name"): ("$" + str(o.get("price")), o.get("description")) for o in ld.get("makesOffer", [])}
        if got_offers != want_offers:
            for k in sorted(set(got_offers) | set(want_offers)):
                if got_offers.get(k) != want_offers.get(k):
                    errors.append(f"{name}: JSON-LD offer {k!r} is {got_offers.get(k)}, site-facts.md says {want_offers.get(k)}")
    errors += check_photos(parsed, FACTS_FILE.read_text())
    return errors


def check_photos(parsed: dict[str, "Page"], facts_md: str) -> list[str]:
    """Every sample photo carries its visible tag and has a complete checklist row, and every row has a sample."""
    errors: list[str] = []
    block = re.search(re.escape(PHOTOS_START) + r"(.*?)" + re.escape(PHOTOS_END), facts_md, re.S)
    if not block:
        return [f"site-facts.md: the 'Photos Devin needs to provide' table ({PHOTOS_START} ... {PHOTOS_END}) is missing"]
    listed: set[str] = set()
    for row in block.group(1).splitlines():
        if not row.startswith("| `"):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        slot = cells[0].strip("`")
        if slot in listed:
            errors.append(f"site-facts.md: photo row {slot!r} appears twice")
        listed.add(slot)
        if len(cells) != 6 or not all(cells):
            errors.append(f"site-facts.md: photo row {slot!r} needs all six cells (slot, where, subject, orientation, size, sample source)")
    used: set[str] = set()
    css = (ROOT / "style.css").read_text() if (ROOT / "style.css").exists() else ""
    for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", css):
        if "ph-tag" in sel and HIDE_RE.search(re.sub(r"\s", "", body.lower())):
            errors.append(f"style.css: a rule for {sel.strip()!r} hides the sample-photo tag")
    for name, page in parsed.items():
        for line, problem in page.photo_problems:
            errors.append(f"{name}:{line}: {problem}")
        for line, url in page.loose_ph:
            errors.append(f"{name}:{line}: sample photo {url} is not inside a <figure class=\"ph\"> with its tag")
        for fig in page.figures:
            where = f"{name}:{fig['line']}"
            if fig["ph"] and not fig["imgs"]:
                errors.append(f"{where}: <figure class=\"ph\"> has no sample photo; remove the class and the tag once the real photo is in")
            if not fig["imgs"]:
                continue
            if not fig["ph"]:
                errors.append(f"{where}: a sample photo's <figure> needs class=\"ph\" so its tag shows")
            if fig["hidden"]:
                errors.append(f"{where}: a sample photo's <figure> is hidden")
            tags = [g for g in fig["tags"] if " ".join(g["text"].split()) == PH_TAG and not g["hidden"] and not g["markup"]]
            if len(tags) != 1 or len(fig["tags"]) != 1:
                errors.append(f"{where}: a sample photo needs exactly one visible <span class=\"ph-tag\">{PH_TAG}</span>")
            for line, url in fig["imgs"]:
                m = PH_FILE_RE.fullmatch(url)
                if not m:
                    errors.append(f"{name}:{line}: sample photo {url!r} is not named assets/placeholders/<slot>-<width>.webp")
                    continue
                used.add(m.group(1))
                if m.group(1) not in listed:
                    errors.append(f"{name}:{line}: sample photo {m.group(1)!r} is not listed under 'Photos Devin needs to provide'")
    for slot in sorted(listed - used):
        errors.append(f"site-facts.md: photo row {slot!r} has no sample on any page; delete the row once the real photo is in")
    return errors


def locations(facts: dict[str, str]) -> str:
    rows = ["| Fact | Where it appears (file:line) |", "|---|---|"]
    for key, value in facts.items():
        if key == "SMS_ENABLED" or key.endswith("_VISITS"):
            continue
        needles = [value]
        if key == "PHONE_DISPLAY":
            needles.append(f"+1-{facts['PHONE_TEL'][2:5]}-{facts['PHONE_TEL'][5:8]}-{facts['PHONE_TEL'][8:]}")
        if key in ("HOURS_WEEKDAYS", "HOURS_SATURDAY"):
            m = RANGE_RE.search(value)
            needles = [m.group(0), f'"opens": "{to24(m.group(1))}", "closes": "{to24(m.group(2))}"']
        if key in ("SERVICE_CALL", "PLAN_ANNUAL", "PLAN_SEMI", "PLAN_QUARTERLY"):
            needles.append(f'"price": "{value[1:]}"')
        if key == "AREA_JSONLD":
            needles = [f'"name": "{a.strip()}"' for a in value.split(";")]
        if key == "INCORPORATED":
            needles = [f"Incorporated {value}", f'"foundingDate": "{value}"']
        if key == "LICENSED_SINCE":
            needles = [f"full-service work since {value}"]
        hits = []
        for name in PAGES:
            for n, text in enumerate((ROOT / name).read_text().splitlines(), 1):
                if any(nd in text for nd in needles):
                    hits.append(f"{name}:{n}")
        rows.append(f"| {key} | {', '.join(hits) or '(none)'} |")
    return "\n".join(rows)


def main() -> int:
    facts = load_facts()
    current = FACTS_FILE.read_text()
    block = f"{LOC_START}\n{locations(facts)}\n{LOC_END}"
    stale = re.search(re.escape(LOC_START) + r".*?" + re.escape(LOC_END), current, re.S)
    if "--update-locations" in sys.argv:
        FACTS_FILE.write_text(current.replace(stale.group(0), block) if stale else current + "\n" + block + "\n")
        print("site-facts.md locations table rewritten")
        current = FACTS_FILE.read_text()
        stale = re.search(re.escape(LOC_START) + r".*?" + re.escape(LOC_END), current, re.S)
    errors = check(facts)
    if not stale or stale.group(0) != block:
        errors.append("site-facts.md: the 'Where each fact appears' table is stale; run python3 check-facts.py --update-locations")
    for e in errors:
        print("FAIL", e)
    print(f"{len(errors)} problem(s) across {len(PAGES)} pages")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
