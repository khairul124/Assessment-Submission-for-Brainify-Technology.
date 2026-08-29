from urllib.parse import urlparse


def canonical_url(url: str) -> str:
    if not url:
        return ""
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/").lower()


def remove_duplicates(products):
    seen = set()
    unique = []
    for product in products:
        # A product is duplicate if its canonical URL or its ID was already seen
        url_key = canonical_url(product.url)
        if url_key and url_key in seen:
            continue
        if product.id and product.id in seen:
            continue

        if url_key:
            seen.add(url_key)
        if product.id:
            seen.add(product.id)

        unique.append(product)
    return unique
