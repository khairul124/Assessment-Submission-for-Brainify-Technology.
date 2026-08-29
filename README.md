# Assessment-Submission-for-Brainify-Technology

## How I approached this project

First half-hour I spent researching pydantic because I never used it before.I watched some videos and read the docs to understand how to work with it and what are the benefits of using it. video link: https://www.youtube.com/watch?v=XIdQ6gO3Anc&t=131s

---

## What I built

### models.py
I defined the `Product` model using pydantic `BaseModel`. It holds all the fields like id, name, url, installs, rating, review_count, last_updated, category and score.

### parser.py
This is the most important part of the project. The json files are messy and each file use different field names for the same data. So I wrote a `normalize_product()` function that handle all the different schemas.

Some files also have encoding issues — some are UTF-8 and some are latin-1. I try UTF-8 first and fall back to latin-1 if it fails because latin-1 is a superset of ASCII and can handle most characters. If a file is totally broken json I just skip it and print a warning so the whole program doesn't crash.

### scoring.py
This one was easier because all the rules are in the brief. I just create a function that:
1. First check if the product was updated in the last 90 days — if not return 0
2. If yes then calculate the score using installs, rating and reviews with the given formula

### duplication.py
Simple but important — I use a set to track seen IDs and only keep the first occurrence of each product. This is O(n) so it's efficient.

### main.py
Calls everything in order — load products → remove duplicates → score each product → sort by score → take top 10 → generate reports.

### reports.py
Writes the top 10 to both `output/report.json` (machine-readable) and `output/report.txt` (human-readable).

---

## Testing

I wrote tests for all three main modules under `tests/`:

- `test_duplication.py` — 8 tests for the deduplication logic
- `test_scoring.py` — 9 tests for the scoring function (checking staleness, caps, rounding etc)
- `test_parser.py` — 15 tests for the parser (all the different field schemas, date formats, bad json handling)

All 32 tests pass.

```
python -m pytest signal-sifter-takehome/tests/ -v
```

---

## Problems I faced

- The json files use different field names (like `title` vs `name` vs `product_name`) so I had to handle all the cases
- Some files have encoding issues — solved by trying UTF-8 first and falling back to latin-1
- One file (`listing_040.json`) has broken/incomplete json — the parser skips it gracefully
- At some point I found that some files were not saved properly and the code was not working. I used Antigravity to check and fix the issue.

---

## How long it took

It took around 4.5 hours total including the research about pydantic, writing the code, debugging and writing the tests.

I tried not to use AI tools for everything — mostly used ChatGPT website to understand concepts and some tricky parts of parser.py. But when I got stuck on a bug I used Antigravity to debug and fix it. I learned a lot of new things while working on this project.

---

Thanks to Brainify Technology for giving me this opportunity to show my skill.
