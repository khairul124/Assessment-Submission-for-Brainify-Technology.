from parser import load_products
from scoring import calculate_score
from duplication import remove_duplicates
from reports import generate_json_report, generate_text_report

def main():
    products = load_products("data")
    products = remove_duplicates(products)
    scored = []
    for product in products:
        updated = product.model_copy(update={"score": calculate_score(product)})
        scored.append(updated)
    scored.sort(key=lambda p: p.score, reverse=True)
    top10 = scored[:10]
    generate_json_report(top10, "output/report.json")
    generate_text_report(top10, "output/report.txt")
    print(f"Successfully generated — top {len(top10)} products written.")

if __name__ == "__main__":
    main()