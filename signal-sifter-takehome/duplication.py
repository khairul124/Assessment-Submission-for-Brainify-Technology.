def remove_duplicates(products):
    seen = set()
    unique = []
    for product in products:
        if product.id not in seen:
            seen.add(product.id)
            unique.append(product)
    return unique
