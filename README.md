# timetraveler.github.io

Every pull request and every push to `main` runs `check-facts.py` through GitHub Actions (`.github/workflows/check.yml`), which fails when a page drifts from `site-facts.md` (the script's docstring lists every check: phone, hours, prices, license, service area, internal links, sample-photo tags and more). A pull request merges only when that run passes; GitHub runs it against the merge of the PR into `main`, so it tests the merged result.
