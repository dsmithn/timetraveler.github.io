# Site facts: the one list to change first

This file is not part of the website (the `_config.yml` file keeps it off majortomsair.com). It is the single list of the facts that appear on the site, and where each one appears, so a change to hours or prices gets made everywhere at once.

**Devin:** change the value here first, then change the same words in each place listed in the table, using the walkthrough below. Destin runs `check-facts.py` afterwards to catch anything missed. You never need to run it.

## The facts

```facts
PHONE_DISPLAY: (561) 860-3670
PHONE_TEL: +15618603670
EMAIL: office@majortomsair.com
LICENSE: CAC1818226
HOURS_WEEKDAYS: Monday to Friday 8 AM – 4:30 PM
HOURS_SATURDAY: Saturday 9 AM – 12 PM
HOURS_SUNDAY: Closed Sunday
SERVICE_CALL: $99
PLAN_ANNUAL: $149
PLAN_ANNUAL_VISITS: 1
PLAN_ANNUAL_EXTRA_SYSTEM: $50
PLAN_ANNUAL_DISCOUNT: 10%
PLAN_SEMI: $269
PLAN_SEMI_VISITS: 2
PLAN_SEMI_EXTRA_SYSTEM: $100
PLAN_SEMI_DISCOUNT: 10%
PLAN_QUARTERLY: $459
PLAN_QUARTERLY_VISITS: 4
PLAN_QUARTERLY_EXTRA_SYSTEM: $200
PLAN_QUARTERLY_DISCOUNT: 15%
AREA_LINE: All of Palm Beach County, plus Deerfield Beach and Pompano Beach.
AREA_JSONLD: Palm Beach County, FL; Deerfield Beach, FL; Pompano Beach, FL
BBB_RATING: A+
SMS_ENABLED: false
```

`BBB_RATING` was last checked on bbb.org on 2026-10-16. Recheck it before each push that touches the site; ratings change.

Hours are written with an en dash (–) between the times, like `8 AM – 4:30 PM`. Copy the dash from this file rather than typing a hyphen.

## Where each fact appears

Line numbers are kept current by `check-facts.py --update-locations`. A fact can appear in a page twice on one line (for example in the JSON-LD block, the computer-readable part at the top of each page).

<!-- LOCATIONS:START -->
| Fact | Where it appears (file:line) |
|---|---|
| PHONE_DISPLAY | index.html:7, index.html:16, index.html:35, index.html:75, index.html:85, index.html:117, index.html:122, index.html:132, index.html:196, index.html:229, index.html:246, maintenance.html:7, maintenance.html:16, maintenance.html:34, maintenance.html:74, maintenance.html:118, maintenance.html:147, maintenance.html:156, maintenance.html:173, register.html:7, register.html:16, register.html:34, register.html:74, register.html:93, register.html:102, register.html:119 |
| PHONE_TEL | index.html:75, index.html:85, index.html:117, index.html:122, index.html:132, index.html:229, index.html:246, maintenance.html:74, maintenance.html:118, maintenance.html:147, maintenance.html:156, maintenance.html:173, register.html:74, register.html:93, register.html:102, register.html:119 |
| EMAIL | index.html:36, index.html:209, index.html:210, index.html:219, index.html:229, maintenance.html:35, maintenance.html:156, register.html:35, register.html:93, register.html:102 |
| LICENSE | index.html:52, index.html:90, index.html:231, maintenance.html:51, maintenance.html:158, register.html:51, register.html:104 |
| HOURS_WEEKDAYS | index.html:49, index.html:93, index.html:230, maintenance.html:48, maintenance.html:147, maintenance.html:157, register.html:48, register.html:103 |
| HOURS_SATURDAY | index.html:50, index.html:93, index.html:230, maintenance.html:49, maintenance.html:147, maintenance.html:157, register.html:49, register.html:103 |
| HOURS_SUNDAY | index.html:93, index.html:230, maintenance.html:147, maintenance.html:157, register.html:103 |
| SERVICE_CALL | index.html:7, index.html:59, index.html:87, index.html:194, maintenance.html:58, maintenance.html:117, register.html:58 |
| PLAN_ANNUAL | index.html:60, index.html:126, index.html:157, maintenance.html:6, maintenance.html:7, maintenance.html:15, maintenance.html:16, maintenance.html:59, maintenance.html:88, register.html:59 |
| PLAN_ANNUAL_EXTRA_SYSTEM | index.html:60, index.html:158, maintenance.html:59, maintenance.html:91, register.html:59 |
| PLAN_ANNUAL_DISCOUNT | index.html:60, index.html:61, index.html:158, index.html:163, index.html:194, maintenance.html:59, maintenance.html:60, maintenance.html:92, maintenance.html:93, maintenance.html:102, maintenance.html:103, register.html:59, register.html:60 |
| PLAN_SEMI | index.html:61, index.html:162, maintenance.html:7, maintenance.html:16, maintenance.html:60, maintenance.html:98, register.html:60 |
| PLAN_SEMI_EXTRA_SYSTEM | index.html:61, index.html:163, maintenance.html:60, maintenance.html:101, register.html:60 |
| PLAN_SEMI_DISCOUNT | index.html:60, index.html:61, index.html:158, index.html:163, index.html:194, maintenance.html:59, maintenance.html:60, maintenance.html:92, maintenance.html:93, maintenance.html:102, maintenance.html:103, register.html:59, register.html:60 |
| PLAN_QUARTERLY | index.html:62, index.html:167, maintenance.html:7, maintenance.html:16, maintenance.html:61, maintenance.html:108, register.html:61 |
| PLAN_QUARTERLY_EXTRA_SYSTEM | index.html:62, index.html:168, maintenance.html:61, maintenance.html:111, register.html:61 |
| PLAN_QUARTERLY_DISCOUNT | index.html:62, index.html:168, index.html:194, maintenance.html:61, maintenance.html:112, maintenance.html:113, register.html:61 |
| AREA_LINE | index.html:84, index.html:198 |
| AREA_JSONLD | index.html:44, index.html:45, index.html:46, maintenance.html:43, maintenance.html:44, maintenance.html:45, register.html:43, register.html:44, register.html:45 |
| BBB_RATING | index.html:231, maintenance.html:158, register.html:104 |
<!-- LOCATIONS:END -->

## How to change your hours (5 steps)

Example: Saturday hours change from 9 AM – 12 PM to 9 AM – 1 PM. These steps change every file in one commit, so the site never shows two different sets of hours.

1. **Open the web editor.** On github.com, open this repository and press the `.` (period) key. An editor opens in the browser (github.dev) with every file listed on the left.
2. **Change this file first.** Click `site-facts.md` and change the `HOURS_SATURDAY` line to `Saturday 9 AM – 1 PM`.
3. **Change the pages.** Press Ctrl+Shift+F (Cmd+Shift+F on a Mac) to search all files for `9 AM – 12 PM`, type `9 AM – 1 PM` in the Replace box and click Replace All. Then search for `"closes": "12:00"` and replace it with `"closes": "13:00"` (it's in the block near the top of each page that starts with `"@context"`; afternoon times use 24-hour numbers: 1 PM is 13:00, 4:30 PM is 16:30).
4. **Commit once, to a new branch.** Click the branch name (`main`) at the bottom left, choose **Create new branch** and call it `hours-update`. Then click the branch icon on the left (Source Control), type a short note like "Saturday hours to 1 PM", and click **Commit & Push**. Open the pull request GitHub offers. Nothing changes on the live site yet.
5. **Tell Destin.** He runs the check on the pull request, which lists anything that still shows the old hours, fixes it on the same branch and merges it. The live site updates a minute or two after the merge.

Screenshots of these screens are still to be added; they need Devin's own GitHub login to capture.

The home page works out "Office hours today" or "Office closed until ..." by itself from the 24-hour block, in Delray Beach time. You don't edit that sentence.

**Closed for a holiday?** In `index.html`, search for `data-holiday-notice=""` and type your notice between the quotes, for example `data-holiday-notice="Closed today for Thanksgiving. Leave a voicemail."`. Put the first day the notice should show in `data-holiday-from` and the last day in `data-holiday-until`, for example `data-holiday-from="2026-11-26" data-holiday-until="2026-11-26"`. You can set it days ahead: before the first day and after the last day the normal hours line shows by itself, even if nobody empties the quotes. Both dates are required; the check fails on a notice without them.

## Texting (`SMS_ENABLED`)

`SMS_ENABLED` is `false`: the site has no texting links and never mentions texting, so nobody texts a line that can't receive texts. When Devin confirms (561) 860-3670 receives texts, Destin turns it on in one change:

- set `SMS_ENABLED: true` above;
- add `<a class="btn btn-outline" href="sms:+15618603670">Text us</a>` under the Call button in the home page hero, and the same link beside the Call button in the sticky bar at the bottom of the home page;
- change `data-closed-suffix="Leave a voicemail."` to `data-closed-suffix="Leave a voicemail or text us."`;
- add a FAQ answer: "Can I text you? Yes, text (561) 860-3670."

`check-facts.py` fails on any texting mention or `sms:` link while the flag is `false`, and on any `sms:` link to a different number once it is `true`.

## Sources for these facts (checked 2026-10-16)

| Fact | Source |
|---|---|
| Phone, email, hours, prices, extra-system prices, discounts, 14-point checklist | The live majortomsair.com `index.html` (upstream `main`): hours on the "Office Hours" lines ("Mon – Fri: 8 AM – 4:30 PM", "Saturday: 9 AM – 12 PM"), plans "$149 … +$50 each additional", "$269 … +$100 each additional", "$459 … +$200 each additional", "10% off service calls ($99 base)", "15% off service calls ($99 base)" |
| License CAC1818226 | Live site ("Lic. #CAC1818226"). Florida DBPR construction license data file (`CONSTRUCTIONLICENSE_1.csv`, downloaded 2026-10-16): license CAC1818226, licensee DONOHUE, DEVIN J, doing business as MAJOR TOMS AIR REPAIR, LLC, status codes C / A (current, active), first licensed 05/29/2015, expires 08/31/2028. The same file lists MAJOR TOMS AIR REPAIR, LLC as a qualified business (QB), Delray Beach. |
| Service area | Design decision (spec 2026-10-05): Palm Beach County plus the north-Broward cities Deerfield Beach and Pompano Beach, matching the live site's "Palm Beach and north Broward counties" |
| BBB rating | bbb.org profile, checked 2026-10-16: rating A+, not BBB accredited, business started 5/29/2015. The site says "BBB rating: A+" and never "accredited". |
| Reviews (Linda Manni, Steven Swanson, Bonnie Barnes) | Quoted word for word from the live site's reviews section |
| "After working for others for 30 years …" | The Intro on the Major Tom's Facebook page |
