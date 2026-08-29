"""
Tests for scoring.py - calculate_score()
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from scoring import calculate_score

REFERENCE_DATE = date(2026, 9, 1)


class DummyProduct:
    """Minimal stand-in for a Product used in scoring tests."""

    def __init__(self, installs, rating, review_count, last_updated):
        self.installs = installs
        self.rating = rating
        self.review_count = review_count
        self.last_updated = last_updated


class TestCalculateScore:

    def test_fresh_high_quality_product_gets_positive_score(self):
        p = DummyProduct(installs=42000, rating=4.3, review_count=812, last_updated=date(2026, 8, 14))
        score = calculate_score(p)
        assert score > 0

    def test_stale_product_scores_zero(self):
        """Products last updated more than 90 days before reference date score 0."""
        p = DummyProduct(installs=100000, rating=5.0, review_count=5000, last_updated=date(2026, 5, 1))
        assert calculate_score(p) == 0

    def test_exactly_90_days_old_not_zero(self):
        """A product updated exactly 90 days before reference date should still score > 0."""
        fresh_limit = date(2026, 6, 3)  # 90 days before 2026-09-01
        p = DummyProduct(installs=10000, rating=4.0, review_count=200, last_updated=fresh_limit)
        assert calculate_score(p) > 0

    def test_exactly_91_days_old_is_zero(self):
        """A product updated 91 days before reference date should score 0."""
        stale = date(2026, 6, 2)  # 91 days before 2026-09-01
        p = DummyProduct(installs=100000, rating=5.0, review_count=9999, last_updated=stale)
        assert calculate_score(p) == 0

    def test_installs_capped_at_50(self):
        """Install points are capped at 50 (1 000 000 / 1000 = 1000, but cap is 50)."""
        high = DummyProduct(installs=1_000_000, rating=3.0, review_count=0, last_updated=date(2026, 8, 1))
        low  = DummyProduct(installs=50_000,    rating=3.0, review_count=0, last_updated=date(2026, 8, 1))
        # Both should yield the same install contribution (50) → same score
        assert calculate_score(high) == calculate_score(low)

    def test_reviews_capped_at_20(self):
        """Review points are capped at 20 (100 000 / 100 = 1000, but cap is 20)."""
        many  = DummyProduct(installs=0, rating=3.0, review_count=100_000, last_updated=date(2026, 8, 1))
        exact = DummyProduct(installs=0, rating=3.0, review_count=2_000,   last_updated=date(2026, 8, 1))
        assert calculate_score(many) == calculate_score(exact)

    def test_low_rating_reduces_score(self):
        """Ratings below 3.0 produce negative rating points, reducing overall score."""
        low  = DummyProduct(installs=10000, rating=1.0, review_count=100, last_updated=date(2026, 8, 1))
        high = DummyProduct(installs=10000, rating=5.0, review_count=100, last_updated=date(2026, 8, 1))
        assert calculate_score(low) < calculate_score(high)

    def test_score_is_rounded_to_two_decimal_places(self):
        p = DummyProduct(installs=12345, rating=4.1, review_count=333, last_updated=date(2026, 8, 1))
        score = calculate_score(p)
        assert round(score, 2) == score

    def test_zero_installs_zero_reviews_minimum_rating(self):
        """Edge case: no engagement at all with rating exactly 3.0 → score = 0."""
        p = DummyProduct(installs=0, rating=3.0, review_count=0, last_updated=date(2026, 8, 1))
        assert calculate_score(p) == 0.0
