import json
from pathlib import Path
from datetime import datetime
from models import Product

def load_products(data_dir: str):
    products = []
    for file in Path(data_dir).glob("*.jsonl"):
      try:
           try:
              text=file.read_text(encoding="utf-8")
           except UnicodeDecodeError:
                text=file.read_text(encoding="latin-1")
           data=json.loads(text)
           product= normalize_product(data)

           if product:
              product.append(product)
      except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {file.name}")
      except Exception as e:
            print(f"Skipping {file.name}: {e}")
    return products

def normalize_product(data):
    name=(data.get("title") or data.get("name") or data.get("product_name"))
    installs=(data.get("installs") or data.get("install_count")or data.get("stats", {}).get("installs"))
    rating = (data.get("rating") or data.get("stars") or data.get("stats", {}).get("rating"))
    reviews = (data.get("reviews") or data.get("num_ratings") or data.get("stats", {}).get("reviews"))
    updated = (data.get("last_updated") or data.get("updated_at") or data.get("modified"))
    if isinstance(installs, str):
        installs = int(installs.replace(",", ""))

    rating = float(rating)
    reviews = int(reviews)

    if isinstance(updated, int):
        last_updated = datetime.utcfromtimestamp(updated).date()
    else:
        last_updated = datetime.fromisoformat(
            updated.replace("Z", "+00:00")
        ).date()

    return Product(
        id=data["id"],
        name=name,
        url=data["url"],
        installs=installs,
        rating=rating,
        review_count=reviews,
        last_updated=last_updated,
        category=data.get("category", "unknown"),
    )
