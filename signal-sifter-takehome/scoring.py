from datetime import date 
Refference_date=date(2026,9,1)
def calculate_score(product):
    age_days=(Refference_date-product.last_updated).days
    if age_days>90:
        return 0
    installs_point=min(product.installs/1000,50)
    rating_points = (product.rating - 3.0) * 10
    review_points = min(product.review_count / 100, 20)
    return round(installs_point + rating_points+ review_points,2,)