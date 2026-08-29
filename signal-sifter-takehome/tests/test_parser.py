"""
Tests for parser.py - load_products() and normalize_product()
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path
from datetime import date
from models import Product
from parser import load_products, normalize_product


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_json(directory, filename, data):
    """Write a dict as a JSON file inside *directory* and return the path."""
    path = Path(directory) / filename
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Tests for normalize_product()
# ---------------------------------------------------------------------------

class TestNormalizeProduct:

    def _base(self, **overrides):
        base = {
            "id": "test-001",
            "title": "Test Plugin",
            "url": "https://example.com/test",
            "installs": 5000,
            "rating": 4.0,
            "reviews": 200,
            "last_updated": "2026-08-01T00:00:00Z",
            "category": "utilities",
        }
        base.update(overrides)
        return base

    def test_basic_schema_parsed_correctly(self):
        p = normalize_product(self._base())
        assert isinstance(p, Product)
        assert p.id == "test-001"
        assert p.name == "Test Plugin"
        assert p.installs == 5000
        assert p.rating == 4.0
        assert p.review_count == 200
        assert p.last_updated == date(2026, 8, 1)

    def test_alternate_name_field_product_name(self):
        data = self._base()
        del data["title"]
        data["product_name"] = "Alt Name Plugin"
        p = normalize_product(data)
        assert p.name == "Alt Name Plugin"

    def test_alternate_name_field_name(self):
        data = self._base()
        del data["title"]
        data["name"] = "Name Field Plugin"
        p = normalize_product(data)
        assert p.name == "Name Field Plugin"

    def test_installs_as_string_with_commas(self):
        p = normalize_product(self._base(installs="12,345"))
        assert p.installs == 12345

    def test_installs_from_stats_nested(self):
        data = self._base()
        del data["installs"]
        data["stats"] = {"installs": 9999, "rating": 4.0, "reviews": 100}
        p = normalize_product(data)
        assert p.installs == 9999

    def test_rating_from_stars_field(self):
        data = self._base()
        del data["rating"]
        data["stars"] = 4.7
        p = normalize_product(data)
        assert p.rating == 4.7

    def test_reviews_from_num_ratings(self):
        data = self._base()
        del data["reviews"]
        data["num_ratings"] = 777
        p = normalize_product(data)
        assert p.review_count == 777

    def test_date_from_unix_timestamp(self):
        import datetime
        ts = int(datetime.datetime(2026, 7, 15, tzinfo=datetime.timezone.utc).timestamp())
        p = normalize_product(self._base(last_updated=ts))
        assert p.last_updated == date(2026, 7, 15)

    def test_date_from_updated_at_field(self):
        data = self._base()
        del data["last_updated"]
        data["updated_at"] = "2026-06-10T12:00:00Z"
        p = normalize_product(data)
        assert p.last_updated == date(2026, 6, 10)

    def test_slash_separated_date(self):
        p = normalize_product(self._base(last_updated="2026/07/11"))
        assert p.last_updated == date(2026, 7, 11)

    def test_category_defaults_to_unknown(self):
        data = self._base()
        del data["category"]
        p = normalize_product(data)
        assert p.category == "unknown"


# ---------------------------------------------------------------------------
# Tests for load_products()
# ---------------------------------------------------------------------------

class TestLoadProducts:

    def test_loads_valid_json_files(self, tmp_path):
        write_json(tmp_path, "a.json", {
            "id": "lp-001", "title": "Plugin A", "url": "https://example.com/a",
            "installs": 1000, "rating": 4.0, "reviews": 50,
            "last_updated": "2026-08-01T00:00:00Z", "category": "tools",
        })
        products = load_products(str(tmp_path))
        assert len(products) == 1
        assert products[0].id == "lp-001"

    def test_skips_invalid_json_file(self, tmp_path):
        (tmp_path / "bad.json").write_text("NOT JSON", encoding="utf-8")
        write_json(tmp_path, "good.json", {
            "id": "lp-002", "title": "Plugin B", "url": "https://example.com/b",
            "installs": 2000, "rating": 3.5, "reviews": 80,
            "last_updated": "2026-08-05T00:00:00Z",
        })
        products = load_products(str(tmp_path))
        assert len(products) == 1
        assert products[0].id == "lp-002"

    def test_empty_directory_returns_empty_list(self, tmp_path):
        assert load_products(str(tmp_path)) == []

    def test_returns_list_of_product_objects(self, tmp_path):
        write_json(tmp_path, "c.json", {
            "id": "lp-003", "title": "Plugin C", "url": "https://example.com/c",
            "installs": 500, "rating": 4.5, "reviews": 30,
            "last_updated": "2026-08-10T00:00:00Z",
        })
        products = load_products(str(tmp_path))
        assert all(isinstance(p, Product) for p in products)

    def test_loads_multiple_files(self, tmp_path):
        for i in range(1, 4):
            write_json(tmp_path, f"p{i}.json", {
                "id": f"m-00{i}", "title": f"Plugin {i}", "url": f"https://example.com/{i}",
                "installs": i * 1000, "rating": 4.0, "reviews": i * 10,
                "last_updated": "2026-08-15T00:00:00Z",
            })
        products = load_products(str(tmp_path))
        assert len(products) == 3
