import json
from pathlib import Path


def generate_json_report(products, output_file):
    data = []

    for rank, product in enumerate(products, start=1):
        data.append(
            {
                "rank": rank,
                "name": product.name,
                "score": product.score,
                "installs": product.installs,
                "rating": product.rating,
                "reviews": product.review_count,
                "last_updated": str(product.last_updated),
            }
        )

    Path(output_file).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def generate_text_report(products, output_file):
    lines = ["SIGNAL SIFTER REPORT", ""]

    for rank, product in enumerate(products, start=1):
        lines.extend(
            [
                f"{rank}. {product.name}",
                f"   Score: {product.score}",
                f"   Installs: {product.installs}",
                f"   Rating: {product.rating}",
                f"   Reviews: {product.review_count}",
                f"   Updated: {product.last_updated}",
                "",
            ]
        )

    Path(output_file).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )