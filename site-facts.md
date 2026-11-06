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
INCORPORATED: 2014
LICENSED_SINCE: 2015
SMS_ENABLED: false
```

`INCORPORATED` and `LICENSED_SINCE` make the footer line "Incorporated 2014, licensed for installs and full-service work since 2015" on every page, and `foundingDate` in the JSON-LD. The site never mentions the BBB: the business is not BBB accredited (Devin, 2026-10-28), so no rating appears, and `check-facts.py` fails on any BBB mention or bbb.org link.

Hours are written with an en dash (–) between the times, like `8 AM – 4:30 PM`. Copy the dash from this file rather than typing a hyphen.

## Where each fact appears

Line numbers are kept current by `check-facts.py --update-locations`. A fact can appear in a page twice on one line (for example in the JSON-LD block, the computer-readable part at the top of each page).

<!-- LOCATIONS:START -->
| Fact | Where it appears (file:line) |
|---|---|
| PHONE_DISPLAY | index.html:7, index.html:16, index.html:37, index.html:76, index.html:103, index.html:148, index.html:157, index.html:176, index.html:248, index.html:282, index.html:299, maintenance.html:7, maintenance.html:16, maintenance.html:35, maintenance.html:74, maintenance.html:118, maintenance.html:153, maintenance.html:162, maintenance.html:179, register.html:7, register.html:16, register.html:35, register.html:74, register.html:93, register.html:102, register.html:119 |
| PHONE_TEL | index.html:76, index.html:103, index.html:148, index.html:157, index.html:176, index.html:282, index.html:299, maintenance.html:74, maintenance.html:118, maintenance.html:153, maintenance.html:162, maintenance.html:179, register.html:74, register.html:93, register.html:102, register.html:119 |
| EMAIL | index.html:38, index.html:262, index.html:263, index.html:272, index.html:282, maintenance.html:36, maintenance.html:162, register.html:36, register.html:93, register.html:102 |
| LICENSE | index.html:54, index.html:115, index.html:284, maintenance.html:52, maintenance.html:164, register.html:52, register.html:104 |
| HOURS_WEEKDAYS | index.html:51, index.html:108, index.html:283, maintenance.html:49, maintenance.html:153, maintenance.html:163, register.html:49, register.html:103 |
| HOURS_SATURDAY | index.html:52, index.html:109, index.html:283, maintenance.html:50, maintenance.html:153, maintenance.html:163, register.html:50, register.html:103 |
| HOURS_SUNDAY | index.html:283, maintenance.html:153, maintenance.html:163, register.html:103 |
| SERVICE_CALL | index.html:7, index.html:60, index.html:112, index.html:246, maintenance.html:58, maintenance.html:117, register.html:58 |
| PLAN_ANNUAL | index.html:61, index.html:166, index.html:209, maintenance.html:6, maintenance.html:7, maintenance.html:15, maintenance.html:16, maintenance.html:59, maintenance.html:88, register.html:59 |
| PLAN_ANNUAL_EXTRA_SYSTEM | index.html:61, index.html:210, maintenance.html:59, maintenance.html:91, register.html:59 |
| PLAN_ANNUAL_DISCOUNT | index.html:61, index.html:62, index.html:210, index.html:215, index.html:246, maintenance.html:59, maintenance.html:60, maintenance.html:92, maintenance.html:93, maintenance.html:102, maintenance.html:103, register.html:59, register.html:60 |
| PLAN_SEMI | index.html:62, index.html:214, maintenance.html:7, maintenance.html:16, maintenance.html:60, maintenance.html:98, register.html:60 |
| PLAN_SEMI_EXTRA_SYSTEM | index.html:62, index.html:215, maintenance.html:60, maintenance.html:101, register.html:60 |
| PLAN_SEMI_DISCOUNT | index.html:61, index.html:62, index.html:210, index.html:215, index.html:246, maintenance.html:59, maintenance.html:60, maintenance.html:92, maintenance.html:93, maintenance.html:102, maintenance.html:103, register.html:59, register.html:60 |
| PLAN_QUARTERLY | index.html:63, index.html:219, maintenance.html:7, maintenance.html:16, maintenance.html:61, maintenance.html:108, register.html:61 |
| PLAN_QUARTERLY_EXTRA_SYSTEM | index.html:63, index.html:220, maintenance.html:61, maintenance.html:111, register.html:61 |
| PLAN_QUARTERLY_DISCOUNT | index.html:63, index.html:220, index.html:246, maintenance.html:61, maintenance.html:112, maintenance.html:113, register.html:61 |
| AREA_LINE | index.html:102, index.html:250 |
| AREA_JSONLD | index.html:46, index.html:47, index.html:48, maintenance.html:44, maintenance.html:45, maintenance.html:46, register.html:44, register.html:45, register.html:46 |
| INCORPORATED | index.html:33, index.html:284, maintenance.html:31, maintenance.html:164, register.html:31, register.html:104 |
| LICENSED_SINCE | index.html:284, maintenance.html:164, register.html:104 |
<!-- LOCATIONS:END -->

## How to change your hours (5 steps)

Example: Saturday hours change from 9 AM – 12 PM to 9 AM – 1 PM. These steps change every file in one commit, so the site never shows two different sets of hours.

1. **Open the web editor.** On github.com, open this repository and press the `.` (period) key. An editor opens in the browser (github.dev) with every file listed on the left.
2. **Change this file first.** Click `site-facts.md` and change the `HOURS_SATURDAY` line to `Saturday 9 AM – 1 PM`.
3. **Change the pages.** Press Ctrl+Shift+F (Cmd+Shift+F on a Mac) to search all files for `9 AM – 12 PM`, type `9 AM – 1 PM` in the Replace box and click Replace All. Then search for `"closes": "12:00"` and replace it with `"closes": "13:00"` (it's in the block near the top of each page that starts with `"@context"`; afternoon times use 24-hour numbers: 1 PM is 13:00, 4:30 PM is 16:30).
4. **Commit once, to a new branch.** Click the branch name (`main`) at the bottom left, choose **Create new branch** and call it `hours-update`. Then click the branch icon on the left (Source Control), type a short note like "Saturday hours to 1 PM", and click **Commit & Push**. Open the pull request GitHub offers. Nothing changes on the live site yet.
5. **Tell Destin.** He runs the check on the pull request, which lists anything that still shows the old hours, fixes it on the same branch and merges it. The live site updates a minute or two after the merge.

Screenshots of these screens are still to be added; they need Devin's own GitHub login to capture.

The home page's "Office Hours" box under the Call button is Devin's own text from his original site, word for word: "Mon – Fri: 8 AM – 4:30 PM" and "Saturday: 9 AM – 12 PM · Messages answered within 24 hours". When the hours change, change those times too (the search in step 3 finds them). The page no longer works out an "open now" or "closed until" line by itself, and there is no holiday notice.

## Texting (`SMS_ENABLED`)

`SMS_ENABLED` is `false`: the site has no texting links and never mentions texting, so nobody texts a line that can't receive texts. When Devin confirms (561) 860-3670 receives texts, Destin turns it on in one change:

- set `SMS_ENABLED: true` above;
- add `<a class="btn btn-outline" href="sms:+15618603670">Text us</a>` under the Call button in the home page hero, and the same link beside the Call button in the sticky bar at the bottom of the home page;
- add a FAQ answer: "Can I text you? Yes, text (561) 860-3670."

`check-facts.py` fails on any texting mention or `sms:` link while the flag is `false`, and on any `sms:` link to a different number once it is `true`.

## Photos Devin needs to provide

The site shows six **sample photos** until Devin sends his own. Each one carries a small "Sample photo, replace with yours" tag in its corner on the live page, so nobody mistakes a stock photo for his work. Real photos of his own jobs, his van and his town will always beat these.

**Devin:** take each photo below on your phone (landscape, in daylight, no customers' faces, house numbers or other companies' names in the frame) and send it to Destin. **Destin** crops it to 3:2, saves `assets/photos/<slot>-480.webp` and `-800.webp` (each 60 KB or less), points the page's `<img>` at them, removes the tag and the `ph` class from that `<figure class="photo ph">` (it keeps `photo`), and deletes the row here. `check-facts.py` fails if any image under `assets/placeholders/` lacks its tag or its row, or if a row here no longer matches a sample on a page.

<!-- PHOTOS:START -->
| Slot | Where it shows | What to photograph | Orientation | Size | Sample in place now |
|---|---|---|---|---|---|
| `ac-repair` | Home page, "AC repair" card | Your hands (or a tech's) on a gauge set at a customer's outdoor unit | Landscape, 3:2 | At least 1600 × 1067 px | Pexels photo 5463580 by José Andrés Pacheco Cortes, https://www.pexels.com/photo/man-repairing-an-aircon-5463580/ (Pexels License), cropped to the hands |
| `new-system` | Home page, "New systems" card | A new condenser you installed beside a stucco house, with the pad and line set showing | Landscape, 3:2 | At least 1600 × 1067 px | Pexels photo 4119844 by Curtis Adams, https://www.pexels.com/photo/facade-of-a-house-4119844/ (Pexels License), cropped |
| `maintenance` | Home page, "Maintenance plans" card | A thermostat on a customer's wall, brand name out of frame | Landscape, 3:2 | At least 1600 × 1067 px | Pexels photo 27638181 by Alexander Mass, https://www.pexels.com/photo/a-digital-thermostat-on-a-wall-next-to-a-window-27638181/ (Pexels License), cropped, maker's mark blurred |
| `commercial` | Home page, "Commercial" card | A rooftop or wall unit at a business you service, with no business sign in frame | Landscape, 3:2 | At least 1600 × 1067 px | Pexels photo 16600100 by aboodi vesakaran, https://www.pexels.com/photo/minimal-background-16600100/ (Pexels License), cropped, maker's logo blurred |
| `street` | Home page, "Family owned and operated" | A Delray Beach street at golden hour, or the van parked on a local street | Landscape, 3:2 | At least 1600 × 1067 px | Unsplash photo LamrkBdQAdY by Dmytro Koplyk, https://unsplash.com/photos/sunset-over-a-coastal-road-with-houses-LamrkBdQAdY (Unsplash License) |
| `attic` | Maintenance plans page, beside the checklist | An attic air handler you serviced, panel off, drain pan showing | Landscape, 3:2 | At least 1600 × 1067 px | Unsplash photo 8JzTjhJWYF0 by Sebastian Herrmann, https://unsplash.com/photos/brown-wooden-attic-8JzTjhJWYF0 (Unsplash License) |
<!-- PHOTOS:END -->

Licences (checked 2026-10-16): Pexels, "All photos and videos on Pexels are free to use. Attribution is not required." Unsplash, "free, including for commercial purposes, without permission from or attributing the photographer or Unsplash." The Pexels licence also says "Don't imply endorsement of your product by people or brands on the imagery", which is one reason no sample shows a face or a readable brand.

## Sources for these facts (checked 2026-10-16)

| Fact | Source |
|---|---|
| Phone, email, hours, prices, extra-system prices, discounts, 14-point checklist | The live majortomsair.com `index.html` (upstream `main`): hours on the "Office Hours" lines ("Mon – Fri: 8 AM – 4:30 PM", "Saturday: 9 AM – 12 PM"), plans "$149 … +$50 each additional", "$269 … +$100 each additional", "$459 … +$200 each additional", "10% off service calls ($99 base)", "15% off service calls ($99 base)" |
| License CAC1818226 | Live site ("Lic. #CAC1818226"). Florida DBPR construction license data file (`CONSTRUCTIONLICENSE_1.csv`, downloaded 2026-10-16): license CAC1818226, doing business as MAJOR TOMS AIR REPAIR, LLC, status codes C / A (current, active), first licensed 05/29/2015, expires 08/31/2028. The same file lists MAJOR TOMS AIR REPAIR, LLC as a qualified business (QB), Delray Beach. |
| Service area | Design decision (spec 2026-10-05): Palm Beach County plus the north-Broward cities Deerfield Beach and Pompano Beach, matching the live site's "Palm Beach and north Broward counties" |
| Incorporated 2014, licensed for installs and full-service work since 2015 | Devin (Discord, 2026-10-28). The DBPR file's first-licensed date, 05/29/2015, agrees with the 2015 half. The site does not mention the BBB: the business is not accredited (Devin, same message). |
| Reviews (Linda Manni, Steven Swanson, Bonnie Barnes) | Quoted word for word from the live site's reviews section. Each is signed with a dash and the reviewer's name only ("— Linda Manni"), the way the live site signs them (:915, :920, :925). |
| "After working for others for 30 years …" | The Intro on the Major Tom's Facebook page. Tom's words (Devin, Discord, 2026-10-28). The page signs it "— Tom": he started the business, and the quote is his. Where it was found is recorded here and is not printed on the page. |
| A Nextdoor neighbor's quote (not on the site) | Waiting on the owner's OK (open question 9). If it goes in, it sits after the two reviews near the bottom of the home page, is signed with the neighbor's name only like the others, and the heading "Two more reviews." changes with it. Without a name it stays off the site. |

## Lines on the pages that come from the owner's own site or his answers (checked 2026-11-04)

Prose lines that make a claim, with where each came from. Line numbers refer to the text of the live majortomsair.com `index.html` (upstream `main`, 2026-06-02).

**How the pages speak (2026-11-05).** The pages are the family talking about their own business: "we", "us", "our", never "Major Tom's does …" or "he". The name stays where it is a name: the logo, page titles, the headline "Call Major Tom's.", the radio lines, the footer block, the licence line and the computer-readable block. A quote is signed with a dash and a name. Where a quote or a fact was found ("on the Facebook page", "per …", "via …") is a source note: it goes in this file and never on a page. The "we" is the family business as a whole.

| Line on the new pages | Source |
|---|---|
| "Office Hours", "Mon – Fri: 8 AM – 4:30 PM", "Saturday: 9 AM – 12 PM · Messages answered within 24 hours" (home page, under the Call button) | His original site, word for word (upstream commit 4bc8c6b, index.html:949-951, the contact block). Put back on 2026-11-06 on the owner's decision; it replaces the line the page used to work out by itself ("Office hours today …" / "Office closed until … Leave a voicemail."), which was our wording, removed with its holiday notice. |
| "2-hour arrival windows" | His trust pill "2-Hour Arrival Windows" (:708); Linda's review (:914) describes one |
| "No call centers. No commissions. Family-owned." and the "No commissions" fact | His line :779 "No call centers. No commissions. Family-owned. Licensed, insured, and straight with you about what it'll actually cost." and :815 "Residential and commercial. No commissions. No surprises on the invoice." |
| "Family owned and operated" / "Family-owned" | Printed on his van (the photo on every page) and in his line :779 |
| "$99 service call to diagnose (repairs quoted before work)" | $99 and "diagnose" from his site (:785 "We diagnose and fix", "10% off service calls ($99 base)"); "repairs quoted before work" is the Phase 1 draft's reading of his :779 "straight with you about what it'll actually cost" and :815 "No surprises on the invoice". Still worth his explicit OK. |
| "All makes and models, at homes and businesses" | :785 "We diagnose and fix all makes and models at your home or office" |
| "Same-day service is available by phone" | :785 "Same-day available by phone", :786 "Same-Day by Phone", :942 "Same-day service by phone only" |
| "Replacement systems, new construction and remodels. Estimates are free, and we clean up before we leave." | :797 "From system replacement to new builds and remodels ... we leave the job site cleaner than we found it. Free estimates." (:798 "Free Estimates") |
| Brands "Carrier, Rheem, Ruud, Tempstar and Trane" | His brands row (:822 onward) |
| "1 visit a year (fall or spring)", "2 visits a year (fall and spring)" | His plan cards :852 "Fall or Spring visit", :865 "Fall AND Spring visits" |
| "If it's urgent, call." (contact section) | :942 "Same-day service by phone only" and :786 "Same-Day by Phone": the phone is his fast path |
| "You'll need the serial number and model number from your install invoice." (register page) | His own register.html: "You'll need your serial number and model number from your install invoice." |
| "We work on offices and other businesses, not just homes." | :815 "Residential and commercial."; his "Residential + Commercial" badge |
| "Major Tom's Air Repair is a family-owned HVAC contractor serving Palm Beach and north Broward counties. Our philosophy is simple: call back, show up, and honest about what it costs." (About section) | His original site, word for word (upstream commit 4bc8c6b, index.html:814), grammar left as he wrote it. Put back on 2026-11-05 on the owner's decision ("use Devin's own line"). It replaces the sentence "Our dad, Tom, started Major Tom's. We work alongside him.", which was our wording and never his, removed on the same decision, and the separate tidied philosophy line ("be" added). Open question 9 is resolved for the family sentence by removal; the Nextdoor quote part of question 9 is still open. |
| "Our mascot" (Bumble alt), "Our van" (van photo alt and the share-image alt on all three pages) | Same things as before, said by the business: "the Major Tom's mascot", "The Major Tom's Air Repair van". Reworded 2026-11-05. |
| "… a new Tempstar or Rheem system we installed." (register page description) | His own register.html offers the Tempstar and Rheem registration links to his install customers ("from your install invoice"). Reworded from "installed by Major Tom's Air Repair" on 2026-11-05. |
| "It's not the heat, it's the humidity!", "The AC guy your neighbors recommend.", "About Us", "Reach Out", "Ground control, this is Major Tom.", "Ground control — it's cold in here!" | His own headings, slogans and bubble (:791, :813, :814, :842, :719) and robots.txt. Cut on 2026-11-04 as filler (slop pass): "Honest people. Honest service." (:701), "Full-service HVAC, done right." (:777), "Your system works hard." (:791), "Stay ahead of the Florida heat." (:909), "They said it better than we could.", "Let's get your AC sorted." (:935). |
| "Ground control to Major Tom:", "AC stopped cooling? Call Major Tom's.", "Major Tom's here. Copy that.", "Mission readout", "Mission list", "Four kinds of call we answer.", "Fig. 1: the vehicle.", "Pick how often we come out.", "Two more reviews.", "Or email the office." | Voice lines written for the redesign (direction A, 2026-11-02; headline from the Phase 1 draft; the last three from the 2026-11-04 slop pass). They name no price, time, rating, year or guarantee. |
