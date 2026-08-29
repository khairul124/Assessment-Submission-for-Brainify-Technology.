# Design Decisions

## Parser (`parser.py`)

### Encoding Strategy
Some JSON files use Latin-1 characters (e.g. accented letters in product names). I try UTF-8 first and fall back to `latin-1` on `UnicodeDecodeError`, since Latin-1 is a superset of ASCII and correctly decodes any single-byte sequence that is not valid UTF-8. Files with truly corrupt bytes are skipped gracefully with a warning.

### Field Normalisation
The data set contains at least three different schemas for the same logical field:
- **Name**: `title` → `name` → `product_name` (checked in that priority order)
- **Installs**: `installs` → `install_count` → `stats.installs`; string values with commas (e.g. `"12,345"`) are parsed to int
- **Rating**: `rating` → `stars` → `stats.rating`
- **Reviews**: `reviews` → `num_ratings` → `stats.reviews`
- **Date**: `last_updated` → `updated_at` → `modified`; UNIX epoch integers and ISO-8601 strings are both supported

Any file that cannot be decoded as JSON is silently skipped so a single corrupt file does not abort the whole run.

## Deduplication (`duplication.py`)

Duplicates are identified by `product.id`. When the same ID appears more than once, only the **first occurrence** (in file-system order) is kept. This is O(n) using a `set` for seen IDs.

## Scoring (`scoring.py`)

Each product receives a score based on three signals:

| Signal | Formula | Cap |
|--------|---------|-----|
| Installs | `installs / 1000` | 50 pts |
| Rating | `(rating - 3.0) × 10` | none (can be negative) |
| Reviews | `review_count / 100` | 20 pts |

Products whose `last_updated` date is more than **90 days** before the reference date (2026-09-01) receive a score of **0**, as stale plugins are considered unreliable signals regardless of their other metrics.

The reference date is hard-coded to 2026-09-01 rather than `date.today()` so that scoring is deterministic and reproducible.

## Report Generation (`reports.py`)

Two output formats are generated:
- **JSON** (`output/report.json`): machine-readable, suitable for downstream pipelines
- **Plain text** (`output/report.txt`): human-readable summary for quick review

Both files are written with explicit `encoding="utf-8"` to avoid platform-specific encoding issues on Windows.

## Testing

Tests are organised under `tests/` with one file per module:

- `test_duplication.py` – 8 tests covering empty input, all-duplicate, mixed, ordering, and type correctness
- `test_scoring.py` – 9 tests covering staleness cut-off (90 vs 91 days), install/review caps, rating impact, rounding, and edge-case zero score
- `test_parser.py` – 15 tests covering all alternate field schemas, date formats, bad JSON handling, and multi-file loading via `tmp_path`

All 32 tests pass with `pytest` (0 failures, 1 deprecation warning from the stdlib `utcfromtimestamp` call in `parser.py`).
