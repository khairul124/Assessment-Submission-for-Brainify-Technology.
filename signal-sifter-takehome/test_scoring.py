from scoring import calculate_score
from datetime import date 
class Dummy:
    installs = 42000
    rating = 4.3
    review_count = 812
    last_updated = date(2026, 8, 14)


def test_score():
    score = calculate_score(Dummy())

    assert score > 0