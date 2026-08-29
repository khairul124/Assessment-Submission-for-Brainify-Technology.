"""
Tests for duplication.py - remove_duplicates()
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from models import Product
from duplication import remove_duplicates


def make_product(pid, name="Test Product", url=None):
    return Product(
        id=pid,
        name=name,
        url=url or f"https://example.com/{pid}",
        installs=1000,
        rating=4.0,
        review_count=100,
        last_updated=date(2026, 8, 1),
        category="test",
    )


class TestRemoveDuplicates:

    def test_empty_list_returns_empty(self):
        assert remove_duplicates([]) == []

    def test_no_duplicates_returns_all(self):
        products = [make_product("a-001"), make_product("b-002"), make_product("c-003")]
        result = remove_duplicates(products)
        assert len(result) == 3

    def test_all_duplicates_returns_one(self):
        products = [make_product("dup-001")] * 5
        result = remove_duplicates(products)
        assert len(result) == 1
        assert result[0].id == "dup-001"

    def test_some_duplicates_keeps_first_occurrence(self):
        p1 = make_product("x-001", name="Original")
        p2 = make_product("x-001", name="Duplicate")
        p3 = make_product("y-002", name="Unique")
        result = remove_duplicates([p1, p2, p3])
        assert len(result) == 2
        assert result[0].name == "Original"
        assert result[1].id == "y-002"

    def test_duplicates_with_different_id_same_url_with_query_params(self):
        p1 = make_product("cr-100", name="Cache Rocket", url="https://example.com/cache-rocket")
        p2 = make_product("cr-101", name="Cache Rocket", url="https://example.com/cache-rocket?utm_source=email")
        result = remove_duplicates([p1, p2])
        assert len(result) == 1
        assert result[0].id == "cr-100"

    def test_preserves_order(self):
        ids = ["c-003", "a-001", "b-002"]
        products = [make_product(i) for i in ids]
        result = remove_duplicates(products)
        assert [p.id for p in result] == ids

    def test_single_product_returned_unchanged(self):
        products = [make_product("solo-001")]
        result = remove_duplicates(products)
        assert len(result) == 1
        assert result[0].id == "solo-001"

    def test_returns_product_objects(self):
        products = [make_product("obj-001"), make_product("obj-002")]
        result = remove_duplicates(products)
        assert all(isinstance(p, Product) for p in result)

    def test_multiple_groups_of_duplicates(self):
        products = [
            make_product("g1-001"),
            make_product("g2-001"),
            make_product("g1-001"),
            make_product("g2-001"),
            make_product("g3-001"),
        ]
        result = remove_duplicates(products)
        assert len(result) == 3
        ids = [p.id for p in result]
        assert "g1-001" in ids
        assert "g2-001" in ids
        assert "g3-001" in ids
