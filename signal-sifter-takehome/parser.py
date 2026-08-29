import json
from pathlib import Path
from datetime import datetime, timezone
from models import Product


def load_products(data_dir: str):
    products = []
    for file in Path(data_dir).glob("*.json"):
        try:
            try:
                text = file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = file.read_text(encoding="latin-1")
            data = json.loads(text)
            product = normalize_product(data)

            if product:
                products.append(product)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {file.name}")
        except Exception as e:
            print(f"Skipping {file.name}: {e}")
    return products


def normalize_product(data: dict):
    # Field mappings based on schema variations
    name = data.get("title") or data.get("name") or data.get("product_name")
    if name:
        name = str(name).strip()

    stats = data.get("stats", {}) if isinstance(data.get("stats"), dict) else {}

    # Installs
    installs = (
        data.get("installs")
        or data.get("install_count")
        or data.get("active_installs")
        or stats.get("installs")
        or stats.get("install_count")
    )
    if installs is None:
        installs = 0
    elif isinstance(installs, str):
        installs = int(installs.replace(",", "").strip())
    else:
        installs = int(installs)

    # Rating
    rating = (
        data.get("rating")
        or data.get("stars")
        or data.get("score")
        or stats.get("rating")
        or stats.get("stars")
    )
    if rating is None:
        rating = 0.0
    else:
        rating = float(rating)

    # Reviews
    reviews = (
        data.get("reviews")
        or data.get("review_count")
        or data.get("num_ratings")
        or stats.get("reviews")
        or stats.get("review_count")
    )
    if reviews is None:
        reviews = 0
    else:
        reviews = int(reviews)

    # Date
    updated = data.get("last_updated") or data.get("updated_at") or data.get("modified")
    if updated is None:
        last_updated = datetime(1970, 1, 1).date()
    elif isinstance(updated, int):
        last_updated = datetime.fromtimestamp(updated, timezone.utc).date()
    else:
        cleaned_date = str(updated).strip().replace("/", "-").replace("Z", "+00:00")
        last_updated = datetime.fromisoformat(cleaned_date).date()

    return Product(
        id=str(data.get("id", "")),
        name=name or "Unknown Product",
        url=str(data.get("url", "")),
        installs=installs,
        rating=rating,
        review_count=reviews,
        last_updated=last_updated,
        category=data.get("category", "unknown"),
    )
