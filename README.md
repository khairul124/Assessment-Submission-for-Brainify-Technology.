# Signal Sifter

Signal Sifter is a Python command-line program that processes messy product listing JSON files, normalizes the data into a consistent structure, removes duplicate products, calculates a score, and generates a ranked top-10 report.

## Features

* Reads product records from JSON files in the `data/` folder
* Handles different field names for the same information
* Handles numbers provided as strings, such as `"18,300"`
* Handles nested `stats` data
* Parses both ISO-8601 date strings and Unix timestamp formats
* Validates normalized data using Pydantic
* Deduplicates product records by ID
* Calculates product scores using the required formula
* Applies the 90-day staleness rule — stale products score 0
* Generates JSON and human-readable text reports
* Includes tests for important functionality

---

## Project Structure

```text
coding-assessment/
│
├── signal-sifter-takehome/
│   ├── models.py          # Pydantic Product model
│   ├── parser.py          # Loads and normalizes JSON files
│   ├── duplication.py     # Removes duplicate products
│   ├── scoring.py         # Calculates product score
│   ├── reports.py         # Writes output files
│   ├── main.py            # Entry point
│   │
│   ├── data/              # Input JSON files (40 listings)
│   ├── output/            # Generated reports
│   │   ├── report.json
│   │   └── report.txt
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_duplication.py
│       ├── test_parser.py
│       └── test_scoring.py
│
├── requirements.txt
├── README.md
└── decission.md
```

---

## Requirements

* Python 3.10 or newer
* pip

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Program

```bash
cd signal-sifter-takehome
python main.py
```

The program reads all JSON files from the `data/` folder and writes the top-10 ranked products to the `output/` folder.

---

## Output

```text
output/
├── report.json
└── report.txt
```

### JSON Report

Machine-readable. Contains the ranked top-10 products with all fields.

### Text Report

Human-readable summary. Each product entry includes:

* Rank
* Product name
* Score
* Install count
* Rating
* Review count
* Last-updated date

---

## Scoring

The score follows the formula from the assignment:

```text
installs_points = min(installs / 1000, 50)

rating_points = (rating - 3.0) * 10

review_points = min(review_count / 100, 20)

score = installs_points + rating_points + review_points
```

The scoring reference date is fixed at:

```text
2026-09-01
```

Products last updated more than 90 days before this date receive a score of `0`.

---

## Running Tests

```bash
python -m pytest signal-sifter-takehome/tests/ -v
```

The tests cover:

* Score calculation (staleness, caps, rounding, edge cases)
* Data normalization (all alternate field schemas, date formats)
* Deduplication (ordering, first-occurrence, multiple groups)
* File loading (bad JSON skipped, multiple files, empty directory)

All 32 tests pass.

---

## Design Notes

The input JSON files use inconsistent field names for the same data. The parser normalizes everything before validation. For example:

```text
title / name / product_name  →  name

installs / install_count / stats.installs  →  installs

last_updated / updated_at / modified  →  last_updated
```

This lets the rest of the application work with a single consistent `Product` model.

More detailed design decisions, limitations, time spent, and AI usage are documented in `decission.md`.

---

## Clean Machine Setup

1. Clone the repository
2. Make sure Python 3.10+ is installed
3. Create and activate a virtual environment
4. Run `pip install -r requirements.txt`
5. Run `python main.py` from inside `signal-sifter-takehome/`
6. Run `pytest` to execute the tests

No database or external service is required.

---

Thanks to Brainify Technology for giving me this opportunity to show my skill.
