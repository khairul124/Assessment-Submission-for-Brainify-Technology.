# DECISIONS.md

## 1. Hours Actually Spent
Total time spent: **~4.5 hours**.
- **Research (~0.5 - 1 hour)**: Reading Pydantic documentation, watching tutorials on data modeling with BaseModel, and understanding Python datetime parsing.
- **Implementation (~2 hours)**: Writing `models.py`, `parser.py`, `duplication.py`, `scoring.py`, `reports.py`, and `main.py`.
- **Testing & Debugging (~1.5 hours)**: Writing 34 unit tests with pytest, fixing edge cases (encoding, slash-separated dates, URL query parameters), and writing documentation.

---

## 2. What I Decided and Why

### Encoding Strategy
Some JSON files contain characters encoded in Latin-1 (e.g. accented letters). I implemented a fallback: `parser.py` attempts UTF-8 first; if a `UnicodeDecodeError` occurs, it automatically falls back to `latin-1` (which is a superset of ASCII). Totally broken JSON files (like `listing_040.json`) are caught with `json.JSONDecodeError` and skipped gracefully so the entire batch does not fail.

### Schema Normalisation
The raw crawler data contains inconsistent field names for identical concepts:
- **Name**: Checked in order `title` → `name` → `product_name`.
- **Installs**: Checked across `installs`, `install_count`, `active_installs`, and nested `stats.installs`; string numbers with commas (`"18,300"`) are stripped and cast to `int`.
- **Rating**: Checked across `rating`, `stars`, `score`, and nested `stats.rating`.
- **Reviews**: Checked across `reviews`, `review_count`, `num_ratings`, and nested `stats.reviews`.
- **Dates**: Supports ISO-8601 strings, slash-separated dates (`"2026/07/11"`), and Unix epoch timestamps.

### Deduplication
Different scraper generations often assigned different IDs to the same listing (e.g. `cr-100` vs `cr-101` with UTM tracking parameters, or `seo-400` vs `seo-401`). To deduplicate records that refer to the same product, I canonicalized product URLs by stripping query strings and trailing slashes, falling back to product ID. Only the first occurrence is kept, running in $O(n)$ time using a hash set.

### Scoring & Determinism
The scoring formula is strictly implemented per specifications:
- Installs: $\min(\text{installs} / 1000, 50)$
- Rating: $(\text{rating} - 3.0) \times 10$
- Reviews: $\min(\text{review\_count} / 100, 20)$
- Staleness rule: Records updated more than 90 days before `2026-09-01` receive a score of `0.0`.
- The reference date is pinned to `2026-09-01` to ensure deterministic, reproducible results across test environments.

---

## 3. What Was New to Me and How I Got Up to Speed
- **Pydantic**: As someone coming primarily from TypeScript / React / Node.js, Pydantic's `BaseModel` was new to me. I watched tutorial videos (e.g. [Pydantic Tutorial](https://www.youtube.com/watch?v=XIdQ6gO3Anc&t=131s)) and read the official Pydantic documentation to learn how schema validation and field types work.
- **Python datetime parsing**: Learning how Python handles ISO 8601 `Z` offsets, timestamps, and date math cleanly.

---

## 4. Where I Used AI, What It Got Wrong, and What I Changed
- **ChatGPT**: Used to look up Pydantic syntax, date-parsing helpers, and understanding how Python handle multi-schema JSON parsing.
- **Antigravity IDE**: Used to inspect directory structure, identify unsaved files during initial setup, and verify automated pytest runs.
- **What needed fixing**: Initial AI snippets assumed all files were valid UTF-8 and only deduplicated by `product.id`, which missed real-world duplicates that had different IDs across crawler runs (like `cr-100` and `cr-101`). I wrote custom URL normalization and multi-encoding fallback to fix this.

---

## 5. What I Left Out and What I Would Do Next with More Time
- **CLI Arguments**: Add `argparse` / `click` support to allow passing custom input directory paths (`--input`) and output directory paths (`--output`).
- **Fuzzy Name Matching**: Implement Levenshtein / fuzzy string matching to catch products with slight title variations (e.g. `"Smart Form Builder"` vs `"smart form builder "`).
- **Export formats**: Add CSV and Markdown table exporters in `reports.py`.
- **CI/CD**: Add GitHub Actions workflow to run `pytest` automatically on push.

---

## 6. Ambiguities in the Brief and How I Handled Them
- **Missing/Null Fields**: Some listings (e.g. `listing_015.json`, `listing_016.json`, `listing_017.json`) have `null` or missing values for installs, ratings, or reviews. I defaulted missing installs and reviews to `0`, and missing ratings to `0.0`, ensuring Pydantic models validate without crashing.
- **Duplicate IDs vs Duplicate Products**: Scrapers generated different IDs for the same product URLs (with query parameters). I handled this by normalizing URLs (removing query parameters) before checking uniqueness.

---

## 7. Extra Things Done
- **Comprehensive Test Suite**: Wrote 34 unit tests across `test_duplication.py`, `test_scoring.py`, and `test_parser.py` with pytest covering edge cases like slash dates, string installs, caps, staleness boundaries (90 vs 91 days), and bad JSON.
- **Cross-Platform UTF-8 Reporting**: Forced `utf-8` file encoding in `reports.py` so reports generate cleanly on Windows, macOS, and Linux without platform encoding mismatches.
